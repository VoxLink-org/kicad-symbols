export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // === 1. CORS 配置 ===
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    if (url.pathname === "/search") {
      const params = url.searchParams;
      const category = params.get("category"); // 核心参数：类别
      const limit = parseInt(params.get("limit") || "5");

      try {
        // ==========================================
        // 第一步：构建智能 JLC Search 请求
        // ==========================================
        const baseUrl = "https://jlcsearch.tscircuit.com";
        let targetPath = "/components/list.json"; // 默认回退到通用搜索
        let searchParams = new URLSearchParams();

        // 类别映射表 (根据你提供的 OpenAPI 定义)
        const CATEGORY_MAP = {
          resistor: "/resistors/list.json",
          capacitor: "/capacitors/list.json",
          inductor: "/inductors/list.json", // 假设有，如果没有会 fallback
          diode: "/diodes/list.json",
          mosfet: "/mosfets/list.json",
          mcu: "/microcontrollers/list.json",
          led: "/leds/list.json",
          connector: "/headers/list.json", // 简单的连接器映射
          adc: "/adcs/list.json",
          regulator: "/voltage_regulators/list.json"
        };

        // 1. 确定目标 Endpoint
        if (category && CATEGORY_MAP[category]) {
          targetPath = CATEGORY_MAP[category];
        }

        // 2. 智能参数映射 (把通用的 keys 映射到 API 特定的 keys)
        // 遍历所有传入参数并透传
        for (const [key, value] of params) {
          if (key === "category" || key === "limit") continue; // 跳过控制参数
          searchParams.append(key, value);
        }

        // 3. 特殊处理：如果 LLM 传了通用的 'value'，我们需要根据类别改名
        const val = params.get("value");
        if (val) {
           if (category === "resistor") searchParams.append("resistance", val);
           else if (category === "capacitor") searchParams.append("capacitance", val);
           else if (category === "inductor") searchParams.append("inductance", val);
        }

        // 4. 发起请求
        const jlcUrl = `${baseUrl}${targetPath}?${searchParams.toString()}`;
        console.log(`Fetching JLC: ${jlcUrl}`); // 调试日志

        const searchResp = await fetch(jlcUrl);
        if (!searchResp.ok) throw new Error(`JLC API Error: ${searchResp.statusText}`);
        
        let searchData = await searchResp.json();

        // JLC API 返回格式有时是 { resistors: [...] } 有时是 { components: [...] }
        // 我们需要找到那个数组
        let components = [];
        const keys = Object.keys(searchData);
        // 找到第一个是数组的 key (通常就是 payload)
        for (const k of keys) {
            if (Array.isArray(searchData[k])) {
                components = searchData[k];
                break;
            }
        }

        if (components.length === 0) {
          return Response.json([], { headers: corsHeaders });
        }

        // 截取并排序
        let candidates = components
          .sort((a, b) => (b.stock || 0) - (a.stock || 0))
          .slice(0, limit);

        // ==========================================
        // 第二步：EasyEDA 详情增强 (保持不变，这部分很好用)
        // ==========================================
        const lcscCodes = candidates.map(c => `C${c.lcsc}`);
        const formData = new URLSearchParams();
        lcscCodes.forEach(code => formData.append("codes[]", code));

        const detailResp = await fetch("https://pro.easyeda.com/api/devices/searchByCodes", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formData
        });

        const detailData = await detailResp.json();
        const detailMap = new Map();
        if (detailData.success && detailData.result) {
          detailData.result.forEach(item => detailMap.set(item.product_code, item));
        }

        // ==========================================
        // 第三步：合并结果
        // ==========================================
        const finalResults = candidates.map(baseItem => {
          const code = `C${baseItem.lcsc}`;
          const details = detailMap.get(code);
          const attrs = details ? details.attributes : {};
          
          return {
            lcsc_id: code,
            mfr_part: baseItem.mfr,
            package: baseItem.package,
            stock: baseItem.stock,
            price_usd: baseItem.price,
            description: baseItem.description || attrs["LCSC Part Name"] || "",
            datasheet: attrs["Datasheet"] || null,
            manufacturer: attrs["Manufacturer"] || baseItem.manufacturer || "",
            // 这里可以根据 category 提取更具体的参数，目前保持通用
            specs: {
               value: attrs["Resistance"] || attrs["Capacitance"] || attrs["Inductance"] || baseItem.resistance || baseItem.capacitance,
               tolerance: attrs["Tolerance"],
               voltage: attrs["Voltage - Rated"] || attrs["Voltage - Supply"],
               temp: attrs["Operating Temperature"],
               ...baseItem // 把 JLC 返回的特定字段也合并进去 (比如 logic_elements)
            },
            _raw_attributes: attrs 
          };
        });

        return new Response(JSON.stringify(finalResults, null, 2), {
          headers: { "Content-Type": "application/json", ...corsHeaders }
        });

      } catch (err) {
        return Response.json({ error: err.message }, { status: 500, headers: corsHeaders });
      }
    }

    return new Response("Smart JLC Router is running.", { headers: corsHeaders });
  },
};