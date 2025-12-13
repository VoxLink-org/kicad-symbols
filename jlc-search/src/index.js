export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // === 1. CORS 配置 (允许跨域) ===
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    // 只处理 /search
    if (url.pathname === "/search") {
      const query = url.searchParams.get("q"); // 搜索关键词
      const limit = parseInt(url.searchParams.get("limit") || "5"); // 默认只查前5个，避免太慢

      if (!query) {
        return Response.json({ error: "Missing 'q' parameter" }, { status: 400, headers: corsHeaders });
      }

      try {
        // ==========================================
        // 第一步：调用 TSCircuit 搜索基础信息 (库存、价格)
        // ==========================================
        const searchUrl = `https://jlcsearch.tscircuit.com/components/list.json?search=${encodeURIComponent(query)}`;
        const searchResp = await fetch(searchUrl);
        const searchData = await searchResp.json();

        if (!searchData.components || searchData.components.length === 0) {
          return Response.json([], { headers: corsHeaders });
        }

        // 截取前 N 个结果，并按库存排序 (LLM 喜欢有库存的)
        let candidates = searchData.components
          .sort((a, b) => b.stock - a.stock) // 库存从大到小
          .slice(0, limit);

        // ==========================================
        // 第二步：构建 EasyEDA 的批量查询请求
        // ==========================================
        // EasyEDA 需要 "C12345" 格式，但 TSCircuit 返回的是数字 12345
        const lcscCodes = candidates.map(c => `C${c.lcsc}`);

        // 构建 form-data body
        const formData = new URLSearchParams();
        lcscCodes.forEach(code => formData.append("codes[]", code));

        const detailResp = await fetch("https://pro.easyeda.com/api/devices/searchByCodes", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          body: formData
        });

        const detailData = await detailResp.json();
        
        // 创建一个 Map 方便查找详细信息： Key=C12345, Value=Details
        const detailMap = new Map();
        if (detailData.success && detailData.result) {
          detailData.result.forEach(item => {
            detailMap.set(item.product_code, item);
          });
        }

        // ==========================================
        // 第三步：数据合并与清洗
        // ==========================================
        const finalResults = candidates.map(baseItem => {
          const code = `C${baseItem.lcsc}`;
          const details = detailMap.get(code);

          // 提取最有用的详细属性
          const attributes = details ? details.attributes : {};
          
          return {
            lcsc_id: code,
            mfr_part: baseItem.mfr, // 型号
            package: baseItem.package, // 封装
            stock: baseItem.stock,    // 库存
            price_usd: baseItem.price, // 价格
            description: baseItem.description || attributes["LCSC Part Name"] || "",
            datasheet: attributes["Datasheet"] || null,
            manufacturer: attributes["Manufacturer"] || "",
            // 提取关键电气参数 (把 EasyEDA 杂乱的属性整理一下)
            specs: {
              voltage_supply: attributes["Voltage - Supply"],
              operating_temp: attributes["Operating Temperature"],
              resolution: attributes["Resolution(Bits)"],
              interface: attributes["Interface"],
              current_iq: attributes["Quiescent Current (Iq)"]
            },
            // 保留所有原始属性以防万一
            // _raw_attributes: attributes 
          };
        });

        return new Response(JSON.stringify(finalResults, null, 2), {
          headers: {
            "Content-Type": "application/json",
            ...corsHeaders
          }
        });

      } catch (err) {
        return Response.json({ error: err.message }, { status: 500, headers: corsHeaders });
      }
    }

    return new Response("JLCPCB Search Worker is running. Try /search?q=ADS1292", { headers: corsHeaders });
  },
};