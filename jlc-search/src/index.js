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
      const category = params.get("category"); // LLM 传入的类别 alias
      const limit = parseInt(params.get("limit") || "5");

      try {
        // ==========================================
        // 配置表：定义类目路径和特殊参数映射
        // Key 是 LLM 可能会用的简写，Value 是 JLC 的真实路径
        // ==========================================
        const ROUTER_CONFIG = {
          // --- Passives ---
          "resistor": { path: "/resistors/list.json", map: { "value": "resistance" } },
          "capacitor": { path: "/capacitors/list.json", map: { "value": "capacitance" } },
          "inductor": { path: "/inductors/list.json", map: { "value": "inductance" } }, // 假设有
          "potentiometer": { path: "/potentiometers/list.json", map: { "value": "maxResistance" } },
          
          // --- Discrete ---
          "diode": { path: "/diodes/list.json", map: { "type": "diode_type" } },
          "mosfet": { path: "/mosfets/list.json", map: {} },
          "bjt": { path: "/bjt_transistors/list.json", map: {} },
          "led": { path: "/leds/list.json", map: {} },
          
          // --- ICs / Processors ---
          "mcu": { path: "/microcontrollers/list.json", map: { "query": "core" } },
          "arm": { path: "/arm_processors/list.json", map: {} },
          "risc-v": { path: "/risc_v_processors/list.json", map: {} },
          "fpga": { path: "/fpgas/list.json", map: {} },
          
          // --- Power ---
          "ldo": { path: "/ldos/list.json", map: { "voltage": "output_voltage" } },
          "regulator": { path: "/voltage_regulators/list.json", map: { "voltage": "output_voltage" } },
          "buck_boost": { path: "/buck_boost_converters/list.json", map: {} },
          "boost": { path: "/boost_converters/list.json", map: {} },
          
          // --- Analog / Data ---
          "adc": { path: "/adcs/list.json", map: { "bits": "resolution" } },
          "dac": { path: "/dacs/list.json", map: { "bits": "resolution" } },
          "opamp": { path: "/components/list.json", map: {} }, // 暂时没有专门的 OpAmp 列表，回退通用
          "sensor_gas": { path: "/gas_sensors/list.json", map: {} },
          "gyroscope": { path: "/gyroscopes/list.json", map: {} },
          
          // --- Connectors / Electromechanical ---
          "connector": { path: "/components/list.json", map: {} }, // 通用连接器回退
          "header": { path: "/headers/list.json", map: { "value": "pitch" } },
          "usb": { path: "/usb_c_connectors/list.json", map: {} },
          "jst": { path: "/jst_connectors/list.json", map: {} },
          "pcie": { path: "/pcie_m2_connectors/list.json", map: {} },
          "relay": { path: "/relays/list.json", map: {} },
          "switch": { path: "/switches/list.json", map: {} },
          
          // --- Displays ---
          "lcd": { path: "/lcd_display/list.json", map: {} },
          "oled": { path: "/oled_display/list.json", map: {} },
          "led_matrix": { path: "/led_dot_matrix_display/list.json", map: {} },
          "led_segment": { path: "/led_segment_display/list.json", map: {} },
          
          // --- Logic / Interface ---
          "io_expander": { path: "/io_expanders/list.json", map: {} },
          "wifi": { path: "/wifi_modules/list.json", map: {} },
          "analog_mux": { path: "/analog_multiplexers/list.json", map: {} }
        };

        // ==========================================
        // 第一步：构建请求
        // ==========================================
        const baseUrl = "https://jlcsearch.tscircuit.com";
        let targetPath = "/components/list.json"; // 默认回退
        let paramMapping = {}; // 当前类别的参数映射规则

        // 1. 确定路径
        if (category && ROUTER_CONFIG[category]) {
          targetPath = ROUTER_CONFIG[category].path;
          paramMapping = ROUTER_CONFIG[category].map || {};
        } else if (category) {
          // 如果 LLM 传了一个不在简写表里，但可能在原始列表里的名字（比如 "adcs"）
          // 尝试直接拼接，看运气
          targetPath = `/${category.toLowerCase()}/list.json`;
        }

        // 2. 构建 JLC Search 参数
        let searchParams = new URLSearchParams();

        // 遍历所有传入的 URL 参数
        for (const [key, value] of params) {
          if (key === "category" || key === "limit") continue; // 跳过控制参数

          // 检查是否有特殊映射 (例如 value -> resistance)
          if (paramMapping[key]) {
            searchParams.append(paramMapping[key], value);
          } else {
            // 如果是 'q'，在专用接口通常对应 'search' 或特定字段，
            // 但大多数接口支持 search 参数作为关键词过滤
            if (key === "q") {
              searchParams.append("search", value);
            } else {
              // 其他参数直接透传 (例如 package, tolerance)
              searchParams.append(key, value);
            }
          }
        }

        const jlcUrl = `${baseUrl}${targetPath}?${searchParams.toString()}`;
        console.log(`[Proxy] Fetching: ${jlcUrl}`);

        const searchResp = await fetch(jlcUrl);
        
        // 如果专用接口 404 (类目不对)，尝试回退到通用接口
        if (!searchResp.ok) {
           console.log("[Proxy] Specific category failed, fallback to generic search.");
           const fallbackUrl = `${baseUrl}/components/list.json?search=${encodeURIComponent(params.get("q") || params.get("value") || "")}`;
           const fallbackResp = await fetch(fallbackUrl);
           if (!fallbackResp.ok) throw new Error("JLC API Error");
           var searchData = await fallbackResp.json();
        } else {
           var searchData = await searchResp.json();
        }

        // 3. 提取组件列表 (API 返回结构不统一，动态查找数组)
        let components = [];
        // 常见的 Key: 'components', 'resistors', 'capacitors', 'results'
        // 我们遍历对象的值，找到第一个是数组的
        for (const val of Object.values(searchData)) {
            if (Array.isArray(val)) {
                components = val;
                break;
            }
        }

        if (components.length === 0) {
          return Response.json([], { headers: corsHeaders });
        }

        // 4. 排序与截取 (优先库存)
        let candidates = components
          .sort((a, b) => (b.stock || 0) - (a.stock || 0))
          .slice(0, limit);

        // ==========================================
        // 第二步：EasyEDA 详情增强
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
        // 第三步：合并输出
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
            specs: {
               // 尝试智能提取主要参数
               value: attrs["Resistance"] || attrs["Capacitance"] || attrs["Inductance"] || baseItem.resistance || baseItem.capacitance,
               tolerance: attrs["Tolerance"],
               voltage: attrs["Voltage - Rated"] || attrs["Voltage - Supply"] || baseItem.voltage_rating,
               temp: attrs["Operating Temperature"],
               // 保留 baseItem 里特有的有用字段 (如 mcu 的 core, flash)
               ...baseItem
            },
            // 调试用：查看原始属性
            // _raw_attributes: attrs 
          };
        });

        return new Response(JSON.stringify(finalResults, null, 2), {
          headers: { "Content-Type": "application/json", ...corsHeaders }
        });

      } catch (err) {
        return Response.json({ error: err.message }, { status: 500, headers: corsHeaders });
      }
    }

    return new Response("JLCPCB Smart Search API is running.", { headers: corsHeaders });
  },
};