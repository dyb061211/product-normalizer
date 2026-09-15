from ai.schemas import ProductInput
SYSTEM_PROMPT="""
你是电商Listing助手

只允许使用用户明确提供的商品信息

禁止创造没有提供的：
品牌
材质
尺寸
承重
认证
功能

如果信息没有提供，不要猜测
输出JSON
输出英文"""

def build_listing_prompt(
        product:ProductInput
):
    user_prompt=f"""
    This is the relevant information of the product
    sku:{product.sku},
    listing_title:{product.title},
    color:{product.color},
    category:{product.category},
    price:{product.price},
    Output JSON fields:
    - sku
    - listing_title
    - bullet_points
    - description
    bullet_points must be an array containing exactly 3 strings.
    """
    return user_prompt