export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // 1. 处理 CORS (允许跨域调用，方便后续集成到 GPTs 或网页)
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    // 只处理 /search 路径
    if (url.pathname === "/search") {
      const query = url.searchParams.get("q"); // 获取搜索关键词
      const limit = parseInt(url.searchParams.get("limit") || "20"); // 默认返回20条

      if (!query) {
        return Response.json({ error: "Missing 'q' parameter" }, { status: 400 });
      }

      try {
        // === 核心逻辑：智能构建 SQL ===
        // 1. 将搜索词拆分为数组 (例如 "LM393 SOIC" -> ["LM393", "SOIC"])
        const terms = query.trim().split(/\s+/);
        
        // 2. 构建 WHERE 子句
        // 逻辑是：每个关键词都必须出现在 (symbol 或 description 或 keywords 或 attributes) 中
        const conditions = [];
        const params = [];

        for (const term of terms) {
          const likeTerm = `%${term}%`;
          conditions.push(`(
            symbol LIKE ? OR 
            description LIKE ? OR 
            keywords LIKE ? OR 
            value LIKE ? OR
            attributes LIKE ?
          )`);
          // 为上面 5 个 ? 填充同一个关键词
          params.push(likeTerm, likeTerm, likeTerm, likeTerm, likeTerm);
        }

        const whereClause = conditions.join(" AND ");

        // 3. 完整的 SQL
        // 优先展示有库存的，然后按价格排序(可选)，最后按 ID 排序
        const sql = `
          SELECT * FROM components 
          WHERE ${whereClause} 
          ORDER BY stock DESC, price ASC, id ASC 
          LIMIT ?
        `;
        
        params.push(limit); // 最后的参数给 LIMIT

        // 4. 执行查询
        const { results } = await env.DB.prepare(sql).bind(...params).all();

        // 5. 数据清洗
        // 数据库里的 attributes 是 JSON 字符串，解析成对象返给 LLM
        const cleanResults = results.map(row => {
          try {
            row.attributes = JSON.parse(row.attributes);
          } catch (e) {
            row.attributes = {};
          }
          return row;
        });

        return new Response(JSON.stringify(cleanResults, null, 2), {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
          }
        });

      } catch (err) {
        return Response.json({ error: err.message }, { status: 500 });
      }
    }

    // 默认欢迎页
    return new Response("KiCad Library Search API is running! Try /search?q=LM393", {
      headers: { "Content-Type": "text/plain" }
    });
  },
};