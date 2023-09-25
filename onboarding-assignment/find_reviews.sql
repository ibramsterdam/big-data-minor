SELECT r.overall, p.price, c.category_name, p.amazon_id
FROM reviews r
JOIN products p ON r.amazon_id = p.amazon_id
JOIN product_category pc ON p.amazon_id = pc.product_id
JOIN categories c ON pc.category_id = c.category_id;