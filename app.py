import streamlit as st
import json
import time
import random
import string
import requests

st.set_page_config(page_title="LP → YouCan Converter", page_icon="🔄", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Almarai:wght@300;400;700;800&display=swap');
* { font-family: 'Almarai', sans-serif; }
.stApp { direction: rtl; }
h1, h2, h3 { text-align: center; }
.success-box { background: #d4edda; border: 1px solid #c3e6cb; border-radius: 10px; padding: 15px; margin: 10px 0; direction: rtl; }
.error-box { background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 10px; padding: 15px; margin: 10px 0; direction: rtl; }
.info-box { background: #d1ecf1; border: 1px solid #bee5eb; border-radius: 10px; padding: 15px; margin: 10px 0; direction: rtl; }
</style>
""", unsafe_allow_html=True)

st.title("🔄 محوّل Landing Page إلى YouCan")
st.markdown("##### حوّل كود JSON الخاص بأداتك إلى كود YouCan Page Builder تلقائياً")

# ============ HELPERS ============

def gid():
    r = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"PBS-{r}{int(time.time()*1000)}"

def make_title(text, subtitle=None, label="العنوان", font_size="2", text_color="#26292EFF",
               sub_size="1.3", sub_color="#4A4A4AFF", mt="10", mb="10", mr="10", ml="10",
               pt=0, pr="10", pb=0, pl="10", font_weight="bold", text_align="center",
               bg_color="transparent"):
    return {
        "id": gid(), "name": "title",
        "blocks": {
            "parameters": {"text": text, "subtitle": subtitle, "style": "style-1", "url": None},
            "style": {
                "text-alignment": text_align, "font-size": font_size, "text-color": text_color,
                "accent-color": "#ff6e55", "font-family": None, "font-weight": font_weight,
                "text-decoration": "none", "line-height": 150, "letter-spacing": 0,
                "subtitle-text-alignment": text_align, "space-between-title": "10",
                "subtitle-font-size": sub_size, "subtitle-text-color": sub_color,
                "subtitle-font-family": None, "subtitle-font-weight": "normal",
                "subtitle-text-decoration": "none", "subtitle-line-height": 150,
                "subtitle-letter-spacing": 0, "title-alignment": "center",
                "margin-top": mt, "margin-right": mr, "margin-bottom": mb, "margin-left": ml,
                "padding-top": pt, "padding-right": pr, "padding-bottom": pb, "padding-left": pl,
                "background-color": bg_color, "css-content": "{ }"
            }
        },
        "label": label, "children": None
    }

def make_row(children, label="هيكل", bg_color="transparent",
             mt="0", mr="10", mb="10", ml="10", br=0,
             pt=0, pr=0, pb=0, pl=0):
    return {
        "id": gid(), "name": "row",
        "blocks": {
            "parameters": {"rows-gap": 0},
            "style": {
                "section-alignment": "center", "is-full-width": True, "width": None,
                "border-radius-top-left": br, "border-radius-top-right": br,
                "border-radius-bottom-right": br, "border-radius-bottom-left": br,
                "margin-top": mt, "margin-right": mr, "margin-bottom": mb, "margin-left": ml,
                "padding-top": pt, "padding-right": pr, "padding-bottom": pb, "padding-left": pl,
                "background-color": bg_color, "background-image": None,
                "background-repeat": "no-repeat", "background-position": "center",
                "background-size": "cover", "css-content": "{ }"
            }
        },
        "label": label, "children": children
    }

def make_column(children, cols=2, label="أعمدة", width="900", bg_color="#00000000",
                dist=None, gap="20", mt="10", mb="10"):
    if dist is None:
        dist = [60] if cols == 2 else []
    return {
        "id": gid(), "name": "column",
        "blocks": {
            "parameters": {
                "columns": cols, "grid-on-mobile": False, "columns-gap": gap,
                "rows-gap": gap, "columns-distribution": dist
            },
            "style": {
                "section-alignment": "center", "vertical-alignment": "center",
                "is-full-width": False, "width": width, "height": None,
                "border-radius-top-left": 0, "border-radius-top-right": 0,
                "border-radius-bottom-right": 0, "border-radius-bottom-left": 0,
                "margin-top": mt, "margin-right": 0, "margin-bottom": mb, "margin-left": 0,
                "padding-top": 0, "padding-right": 0, "padding-bottom": 0, "padding-left": 0,
                "background-color": bg_color, "background-image": None,
                "background-repeat": "no-repeat", "background-position": "center",
                "background-size": "cover", "css-content": "{ }"
            }
        },
        "label": label, "children": children
    }

def make_spacer(space=10, width="80", color="#1A6B5AFF", thickness="3"):
    return {
        "id": gid(), "name": "spacer",
        "blocks": {
            "parameters": {"space": space, "spacer-style": "divider", "is-shadow": False},
            "style": {
                "spacer-alignment": "center", "is-full-width": False, "width": width,
                "margin-top": 0, "margin-bottom": 0, "divider-thickness": thickness,
                "divider-color": color, "border-style": "solid",
                "background-color": "transparent", "css-content": "{ }"
            }
        },
        "label": "فاصل", "children": None
    }

def make_button(text, target_id, label="زر", bg="#F5A623FF", hover="#E8941AFF",
                icon="fas fa-shopping-cart", sticky_m=False, sticky_d=False,
                width="300", anim="scale"):
    return {
        "id": gid(), "name": "link-button",
        "blocks": {
            "parameters": {
                "content": f"<p><strong>{text}</strong></p>",
                "icon-choice": "font-awesome", "icon-class": icon, "icon-image": None,
                "type": "scroll-to-section", "target-section": target_id,
                "target-external-section": None,
                "sticky-mobile": sticky_m, "sticky-desktop": sticky_d
            },
            "style": {
                "button-alignment": "center", "is-full-width": False, "width": width, "height": None,
                "margin-top": "10", "margin-right": "10", "margin-bottom": "10", "margin-left": "10",
                "padding-top": "10", "padding-right": "10", "padding-bottom": "10", "padding-left": "10",
                "background-color": bg, "hover-background-color": hover,
                "active-background-color": hover,
                "container-desktop-background-color": "transparent",
                "container-mobile-background-color": "transparent",
                "font-size": "18", "line-height": 150, "letter-spacing": 0,
                "text-vertical-alignment": "center", "text-horizontal-alignment": "center",
                "text-color": "#FFFFFF", "hover-text-color": "#FFFFFF", "active-text-color": "#FFFFFF",
                "text-shadow": "0px 0px 0px black",
                "icon-alignment": "row", "icon-size": "20", "icon-color": "#FFFFFF",
                "icon-hover-color": "#FFFFFF",
                "space-in-between": "15", "space-in-between-mobile": 15,
                "icon-shadow": "0px 0px 0px #000000",
                "border-radius-top-left": "30", "border-radius-top-right": "30",
                "border-radius-bottom-right": "30", "border-radius-bottom-left": "30",
                "hover-border-radius-top-left": "30", "hover-border-radius-top-right": "30",
                "hover-border-radius-bottom-right": "30", "hover-border-radius-bottom-left": "30",
                "active-border-radius-top-left": "30", "active-border-radius-top-right": "30",
                "active-border-radius-bottom-right": "30", "active-border-radius-bottom-left": "30",
                "border-width": "0", "hover-border-width": 0, "active-border-width": 0,
                "border-color": "#000000FF", "hover-border-color": "#000000FF",
                "active-border-color": "#000000FF", "border-style": "solid",
                "animation-name": anim, "animation-direction": "from-left-ltr",
                "animation-duration": "1000", "animation-length-from": "0.9",
                "animation-length-to": "1", "animation-timing": "linear",
                "button-shadow": "0px 0px 0px 0px black",
                "hover-button-shadow": "0px 0px 0px 0px black",
                "active-button-shadow": "0px 0px 0px 0px black",
                "css-content": "{ }"
            }
        },
        "label": label, "children": None
    }

def make_image(url, label="صورة", width="100%", alignment="center"):
    return {
        "id": gid(), "name": "image",
        "blocks": {
            "parameters": {
                "image": url, "type": "none",
                "target-section": None, "target-external-section": None
            },
            "style": {
                "image-alignment": alignment, "is-full-width": False, "width": width,
                "height": None,
                "border-t-l-radius": 0, "border-t-r-radius": 0,
                "border-b-r-radius": 0, "border-b-l-radius": 0,
                "margin-top": 0, "margin-right": 0, "margin-bottom": 0, "margin-left": 0,
                "background-color": "transparent", "css-content": "{ }"
            }
        },
        "label": label, "children": None
    }

def make_countdown(hours=24):
    return {
        "id": gid(), "name": "countdown",
        "blocks": {
            "parameters": {
                "style": "style-1",
                "days": 0, "hours": hours, "minutes": 0, "seconds": 0,
                "days-label": "يوم", "hours-label": "ساعة",
                "minutes-label": "دقيقة", "seconds-label": "ثانية",
                "is-days-enabled": False, "is-hours-enabled": True,
                "is-minutes-enabled": True, "is-seconds-enabled": True,
                "s5-promo-text": "عرض محدود 🔥", "s5-button-text": "اطلب الآن"
            },
            "style": {
                "width": "500",
                "countdown-size": "medium",
                "counter-horizontal-alignment": "center",
                "counter-background-color": "#FFFFFFFF",
                "counter-text-color": "#1A6B5AFF",
                "counter-time-color": "#C0392BFF",
                "counter-dots-color": "#333333FF",
                "counter-border-color": "#E0E0E0FF",
                "counter-border-radius": "10",
                "counter-border-width": "1",
                "border-color": "#00000000",
                "border-radius": "15",
                "border-width": "0",
                "progress-bar-color": "#1A6B5AFF",
                "background-color": "#F8F8F8FF",
                "background-image": None,
                "background-repeat": "no-repeat",
                "background-position": "center",
                "background-size": "cover",
                "margin-top": "10", "margin-right": 0, "margin-bottom": "10", "margin-left": 0,
                "padding-top": "15", "padding-right": "15", "padding-bottom": "15", "padding-left": "15",
                "s4-counter-top-color": "#1A6B5AFF",
                "s4-counter-bottom-color": "#145A4BFF",
                "s4-counter-label-bg-color": "#F5F5F5FF",
                "s5-banner-bg-color": "#1A6B5AFF",
                "s5-banner-background-image": None,
                "s5-banner-background-repeat": "no-repeat",
                "s5-banner-background-position": "center",
                "s5-banner-background-size": "cover",
                "s5-button-bg-color": "#F5A623FF",
                "s5-button-text-color": "#FFFFFFFF",
                "s5-counter-timer-text-color": "#FFFFFFFF",
                "s5-counter-timer-label-text-color": "#FFFFFFCC",
                "s5-promo-text-color": "#FFFFFFFF",
                "css-content": "{ }"
            }
        },
        "label": "عداد تنازلي", "children": None
    }

def make_checkout(product_id, variant_id, button_text="اطلب الآن!"):
    return {
        "id": gid(), "name": "express-checkout-form",
        "blocks": {
            "parameters": {
                "product-id": product_id,
                "product-variant-id": variant_id,
                "show-variants-selector": False,
                "show-product-price": True,
                "show-product-compare-at-price": True,
                "button-text": button_text,
                "express-checkout-form-header": '<p style="text-align: center;"><span style="font-size: 28px;"><span style="color: rgb(255, 255, 255);">✨ عرض محدود</span></span></p>',
                "express-checkout-form-pre-footer": '<p style="text-align: center;"><span style="font-size: 14px;"><span style="color: rgb(255, 255, 255);">🛡️ ضمان استرجاع 30 يوم | 🚚 شحن مجاني</span></span></p>',
                "express-checkout-form-footer": ""
            },
            "style": {
                "is-full-width": True, "width": None, "height": None,
                "form-alignment": "center",
                "form-border-color": "#1A6B5AFF", "form-border-radius": "15",
                "form-border-style": "solid", "form-border-width": "2",
                "background-color": "#1A6B5AFF",
                "background-image": None, "background-repeat": "no-repeat",
                "background-position": "center", "background-size": "cover",
                "margin-top": "20", "margin-right": "10", "margin-bottom": "20", "margin-left": "10",
                "padding-top": "20", "padding-right": "20", "padding-bottom": "20", "padding-left": "20",
                "button-background-color": "#F5A623FF",
                "hover-button-background-color": "#E8941AFF",
                "button-text-color": "#FFFFFFFF",
                "hover-button-text-color": "#FFFFFFFF",
                "button-border-color": "#F5A623FF",
                "hover-button-border-color": "#E8941AFF",
                "button-border-radius": "30", "button-border-width": "0",
                "hover-button-border-width": "0",
                "button-font-size": "18",
                "button-padding-horizontal": "30", "button-padding-vertical": "12",
                "image-button-border-color": "#E0E0E0FF",
                "input-background-color": "#FFFFFFFF",
                "input-border-color": "#E0E0E0FF",
                "input-border-radius": "10", "input-border-style": "solid", "input-border-width": "1",
                "input-font-size": "16",
                "input-padding-horizontal": "12", "input-padding-vertical": "10",
                "input-placeholder-color": "#999999FF", "input-text-color": "#333333FF",
                "focus-input-background-color": "#FFFFFFFF",
                "focus-input-border-color": "#1A6B5AFF",
                "focus-input-border-width": "2", "focus-input-text-color": "#333333FF",
                "enable-input-label": True,
                "price-text-color": "#F5A623FF", "price-alignment": "center",
                "price-font-family": None, "price-font-size": "24",
                "price-font-weight": "bold", "price-letter-spacing": 0,
                "price-line-height": 150, "price-text-decoration": "none",
                "price-text-shadow": "0px 0px 0px black",
                "compare-at-price-text-color": "#FFFFFF99",
                "compare-at-price-font-family": None, "compare-at-price-font-size": "16",
                "compare-at-price-font-weight": "normal", "compare-at-price-letter-spacing": 0,
                "compare-at-price-line-height": 150, "compare-at-price-text-decoration": "line-through",
                "compare-at-price-text-shadow": "0px 0px 0px black",
                "radio-button-background-color": "#FFFFFFFF",
                "radio-button-border-color": "#CCCCCCFF",
                "radio-button-checkmark-color": "#1A6B5AFF",
                "color-button-border-color": "#E0E0E0FF",
                "selected-color-button-border-color": "#1A6B5AFF",
                "selected-image-button-border-color": "#1A6B5AFF",
                "textual-button-background-color": "#F5F5F5FF",
                "textual-button-border-color": "#E0E0E0FF",
                "textual-button-text-color": "#333333FF",
                "selected-textual-button-background-color": "#1A6B5AFF",
                "selected-textual-button-border-color": "#1A6B5AFF",
                "selected-textual-button-text-color": "#FFFFFFFF",
                "variant-selector-alignment": "center",
                "variant-selector-direction": "row",
                "css-content": "{ }"
            }
        },
        "label": "نموذج الشراء السريع", "children": None
    }

# ============ CONVERTER ============

def convert_lp_to_youcan(d, product_id, variant_id):
    checkout_id = gid()
    sections = []

    # 1. Notice Bar
    badges = d.get("trust_badges", ["شحن مجاني", "دفع آمن", "جودة مضمونة"])
    sections.append(
        make_row([
            make_title(" | ".join([f"✅ {b}" for b in badges]),
                       label="إشعار", font_size="0.9", text_color="#FFFFFFFF",
                       mt="5", mb="5")
        ], label="شريط الإشعارات", bg_color="#1A6B5AFF")
    )

    # 2. Hero
    hero_children = [
        make_title(d.get("hero_headline", ""), d.get("hero_subheadline"),
                   label="العنوان الرئيسي", font_size="2.2", text_color="#1A6B5AFF",
                   sub_size="1.3", sub_color="#4A4A4AFF", mt="20", mb="10")
    ]
    benefits = d.get("hero_benefits", [])
    if benefits:
        btext = " | ".join([f"✅ {b.get('title', b) if isinstance(b, dict) else b}" for b in benefits])
        hero_children.append(make_title(btext, label="المزايا", font_size="1", text_color="#1A6B5AFF", mt="5", mb="5"))

    sp_num = d.get("social_proof_number", "")
    sp_text = d.get("social_proof_text", "")
    if sp_num or sp_text:
        hero_children.append(make_title(f"{sp_num} {sp_text} ⭐⭐⭐⭐⭐",
                                        label="الدليل الاجتماعي", font_size="1.2",
                                        text_color="#F5A623FF", mt="5", mb="10"))

    cta = d.get("call_to_action", "اطلب الآن!")
    hero_children.append(make_button(cta, checkout_id, label="زر الطلب", anim="scale"))
    sections.append(make_row(hero_children, label="القسم الرئيسي", bg_color="#F5F9F7FF"))

    # 3. Problem
    if d.get("problem_title"):
        prob_children = [
            make_title(d["problem_title"], d.get("problem_description"),
                       label="المشكلة", font_size="2", text_color="#C0392BFF",
                       sub_size="1.2", sub_color="#4A4A4AFF", mt="20", mb="10")
        ]
        points = d.get("problem_points", [])
        if points:
            prob_children.append(make_title("❌ " + "\n❌ ".join(points),
                                           label="نقاط المشكلة", font_size="1.1",
                                           text_color="#C0392BFF", mt="5", mb="15"))
        sections.append(make_spacer())
        sections.append(make_row(prob_children, label="قسم المشكلة", bg_color="#FFF5F5FF", br="20"))

    # 4. Solution
    if d.get("solution_title"):
        sections.append(make_row([
            make_title(d["solution_title"], d.get("solution_description"),
                       label="الحل", font_size="2", text_color="#1A6B5AFF",
                       sub_size="1.2", sub_color="#4A4A4AFF", mt="20", mb="10"),
            make_button("اطلب الآن", checkout_id, bg="#1A6B5AFF", hover="#145A4BFF")
        ], label="قسم الحل", bg_color="#F0FFF4FF", br="20"))

    # 5. Features
    features = d.get("features", [])
    if features:
        feat_children = [make_title("مميزات المنتج", label="عنوان المميزات",
                                    font_size="2.2", text_color="#1A6B5AFF", mt="20", mb="10")]
        for f in features:
            title = f.get("title", f) if isinstance(f, dict) else f
            desc = f.get("desc", f.get("description", "")) if isinstance(f, dict) else ""
            feat_children.append(make_title(title, desc if desc else None,
                                           label=str(title)[:20], font_size="1.5", text_color="#1A6B5AFF",
                                           sub_size="1.1", sub_color="#4A4A4AFF", mt="10", mb="10"))
        sections.append(make_row(feat_children, label="قسم المميزات"))

    # 6. Ingredients
    ingredients = d.get("ingredients", [])
    if ingredients:
        ing_children = [make_title("المكونات الطبيعية", label="عنوان المكونات",
                                   font_size="2", text_color="#1A6B5AFF", mt="20", mb="10")]
        for ing in ingredients:
            name = ing.get("name", ing) if isinstance(ing, dict) else ing
            benefit = ing.get("benefit", "") if isinstance(ing, dict) else ""
            ing_children.append(make_title(str(name), benefit if benefit else None,
                                          label=str(name)[:20], font_size="1.3", text_color="#1A6B5AFF",
                                          sub_size="1", sub_color="#4A4A4AFF", mt="8", mb="8"))
        sections.append(make_row(ing_children, label="قسم المكونات", bg_color="#FFFEF5FF"))

    # 7. How to use
    steps = d.get("how_to_use", [])
    if steps:
        steps_children = [make_title("طريقة الاستخدام", label="عنوان الاستخدام",
                                     font_size="2", text_color="#1A6B5AFF", mt="20", mb="10")]
        for i, step in enumerate(steps):
            steps_children.append(make_title(f"الخطوة {i+1}", step,
                                            label=f"خطوة {i+1}", font_size="1.5", text_color="#1A6B5AFF",
                                            sub_size="1.1", sub_color="#333333FF", mt="8", mb="8"))
        sections.append(make_row(steps_children, label="قسم الاستخدام"))

    # 8. Stats
    stats = d.get("stats", [])
    if stats:
        stat_titles = []
        for stat in stats:
            num = stat.get("number", stat) if isinstance(stat, dict) else stat
            lbl = stat.get("label", "") if isinstance(stat, dict) else ""
            stat_titles.append(make_title(str(num), lbl if lbl else None,
                                         font_size="2.5", text_color="#F5A623FF",
                                         sub_size="1", sub_color="#FFFFFFFF", mt="10", mb="10"))
        sections.append(make_column(stat_titles, cols=len(stats), label="الإحصائيات",
                                    width="850", bg_color="#1A6B5AFF",
                                    dist=[round(100/len(stats)*i) for i in range(1, len(stats))], gap="10"))

    # 9. Doctors
    doctors = d.get("doctors", [])
    if doctors:
        doc_children = [make_title("آراء المختصين", label="عنوان الأطباء",
                                   font_size="2", text_color="#1A6B5AFF", mt="20", mb="10")]
        for doc in doctors:
            name = doc.get("name", "")
            title = doc.get("title", "")
            quote = doc.get("quote", "")
            doc_children.append(make_title(f"{name} - {title}", f'"{quote}"',
                                          label=str(name)[:20], font_size="1.3", text_color="#1A6B5AFF",
                                          sub_size="1.1", sub_color="#333333FF", mt="10", mb="10"))
        sections.append(make_row(doc_children, label="قسم الأطباء", bg_color="#F5F9F7FF"))

    # 10. Reviews
    reviews = d.get("reviews", [])
    if reviews:
        rev_children = [make_title("ماذا يقول عملاؤنا؟", label="عنوان التقييمات",
                                   font_size="2", text_color="#1A6B5AFF", mt="20", mb="10")]
        for rev in reviews:
            name = rev.get("name", "")
            rating = rev.get("rating", 5)
            comment = rev.get("comment", "")
            stars = "⭐" * int(rating)
            rev_children.append(make_title(f"{stars} — {name}", f'"{comment}"',
                                          label=str(name)[:20], font_size="1.2", text_color="#1A6B5AFF",
                                          sub_size="1", sub_color="#333333FF", mt="10", mb="10"))
        sections.append(make_row(rev_children, label="قسم التقييمات", bg_color="#FFFEF5FF"))

    # 11. Urgency + Countdown
    if d.get("urgency_text"):
        sections.append(make_title(d["urgency_text"], label="نص الاستعجال",
                                   font_size="2", text_color="#C0392BFF", mt="20", mb="5"))
    sections.append(make_countdown(d.get("countdown_hours", 24)))

    # 12. Pricing
    pricing = d.get("pricing", {})
    if pricing:
        currency = pricing.get("currency", "")
        orig = pricing.get("original", "")
        disc = pricing.get("discounted", "")
        pct = pricing.get("discount_percent", "")
        sections.append(make_row([
            make_title(f"السعر القديم: {orig} {currency}",
                       f"السعر الجديد: {disc} {currency} — وفر {pct}!",
                       label="السعر", font_size="1.5", text_color="#888888FF",
                       sub_size="2.5", sub_color="#F5A623FF", mt="15", mb="15")
        ], label="قسم السعر"))

    # 13. Express Checkout
    ck = make_checkout(product_id, variant_id, cta)
    ck['id'] = checkout_id
    sections.append(ck)

    # 14. Guarantee
    if d.get("guarantee_title"):
        sections.append(make_row([
            make_title(f"🛡️ {d['guarantee_title']}", d.get("guarantee_text"),
                       label="الضمان", font_size="1.5", text_color="#1A6B5AFF",
                       sub_size="1.1", sub_color="#333333FF", mt="15", mb="15")
        ], label="قسم الضمان", bg_color="#F0FFF4FF", br="20"))

    # 15. FAQ
    faq = d.get("faq", [])
    if faq:
        faq_children = [make_title("الأسئلة الشائعة", label="عنوان FAQ",
                                   font_size="2", text_color="#1A6B5AFF", mt="20", mb="10")]
        for item in faq:
            q = item.get("q", item.get("question", ""))
            a = item.get("a", item.get("answer", ""))
            faq_children.append(make_title(f"❓ {q}", a,
                                          label=str(q)[:20], font_size="1.2", text_color="#1A6B5AFF",
                                          sub_size="1", sub_color="#333333FF", mt="8", mb="8"))
        sections.append(make_row(faq_children, label="قسم الأسئلة الشائعة"))

    # 16. Sticky CTA
    sections.append(make_button(cta, checkout_id, label="زر ثابت",
                                icon="fas fa-shopping-bag", sticky_m=True, sticky_d=True,
                                anim="vertical-bounce"))

    # 17. Footer
    if d.get("footer_text"):
        sections.append(make_title(d["footer_text"], label="الفوتر",
                                   font_size="0.8", text_color="#888888FF", mt="20", mb="20"))

    # Family headline
    if d.get("family_headline") and not any("العائلة" in (s.get("label","")) for s in sections):
        # Insert before FAQ
        faq_idx = next((i for i, s in enumerate(sections) if s.get("label") == "قسم الأسئلة الشائعة"), -1)
        if faq_idx > 0:
            sections.insert(faq_idx, make_row([
                make_title(d["family_headline"], label="العائلة",
                           font_size="1.8", text_color="#1A6B5AFF", mt="20", mb="15")
            ], label="قسم العائلة", bg_color="#F5F9F7FF"))

    return {
        "sections": sections,
        "settings": {
            "page-direction": "rtl", "is-full-width": False, "width": "600",
            "center-elements": True, "background-color": "#FFFFFF",
            "background-image": None, "background-repeat": "no-repeat",
            "background-position": "center", "background-size": "cover",
            "font-family": "Almarai", "font-size-desktop": 16, "font-size-mobile": 12,
            "text-color": "#1a1a1a", "content-alignment": "center",
            "section-alignment": "center",
            "margin-top": 0, "margin-right": 0, "margin-bottom": 0, "margin-left": 0
        }
    }


# ============ UI ============

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 المدخلات")

    input_method = st.radio("طريقة الإدخال:", ["📝 لصق الكود", "📁 رفع ملف JSON"], horizontal=True)

    lp_json_text = ""
    if input_method == "📝 لصق الكود":
        lp_json_text = st.text_area("الصق كود JSON الخاص بالـ Landing Page:", height=300,
                                     placeholder='{"hero_headline": "...", ...}')
    else:
        uploaded = st.file_uploader("ارفع ملف JSON:", type=["json"])
        if uploaded:
            lp_json_text = uploaded.read().decode("utf-8")
            st.success(f"✅ تم رفع: {uploaded.name}")

    st.markdown("---")
    st.subheader("🏪 بيانات المنتج")

    store_url = st.text_input("رابط المتجر (بدون / في النهاية):", 
                               placeholder="https://souklblad.com")
    product_id = st.text_input("Product ID:", 
                                placeholder="e9cf499c-b31f-4aa8-b626-9925b7ee98a0")

    auto_fetch = st.button("🔍 جلب Variant ID تلقائياً")
    variant_id = st.text_input("Variant ID (يتم جلبه تلقائياً):", key="variant_id_input",
                                placeholder="سيتم ملؤه تلقائياً...")

    if auto_fetch and store_url and product_id:
        try:
            api_url = f"{store_url.rstrip('/')}/api/products/{product_id}?include=variants"
            r = requests.get(api_url, timeout=10)
            data = r.json()
            variants = data.get("variants", [])
            if variants:
                vid = variants[0]["id"]
                st.session_state["fetched_variant"] = vid
                st.success(f"✅ تم جلب Variant ID: `{vid}`")
            else:
                st.warning("⚠️ لم يتم العثور على variants")
        except Exception as e:
            st.error(f"❌ خطأ: {e}")

with col2:
    st.subheader("📤 النتيجة")

    convert_btn = st.button("🚀 تحويل الآن", type="primary", use_container_width=True)

    if convert_btn:
        if not lp_json_text.strip():
            st.error("❌ الرجاء إدخال كود JSON")
        elif not product_id.strip():
            st.error("❌ الرجاء إدخال Product ID")
        else:
            try:
                d = json.loads(lp_json_text)
                vid = st.session_state.get("fetched_variant", variant_id.strip())
                if not vid:
                    vid = ""

                result = convert_lp_to_youcan(d, product_id.strip(), vid)
                result_json = json.dumps(result, ensure_ascii=False, indent=2)

                st.success(f"✅ تم التحويل بنجاح! ({len(result['sections'])} قسم)")

                st.download_button(
                    "⬇️ تحميل ملف YouCan JSON",
                    data=result_json,
                    file_name="youcan-landing-page.json",
                    mime="application/json",
                    use_container_width=True
                )

                with st.expander("👁️ معاينة الأقسام"):
                    for i, s in enumerate(result['sections']):
                        icon = {"row": "📦", "title": "📝", "column": "📊", "spacer": "➖",
                                "link-button": "🔘", "countdown": "⏰", "express-checkout-form": "🛒",
                                "image": "🖼️"}.get(s['name'], "📄")
                        children_count = len(s['children']) if s.get('children') else 0
                        extra = f" ({children_count} عنصر)" if children_count else ""
                        st.write(f"{icon} **{i+1}.** {s['label']}{extra}")

                with st.expander("📋 الكود الكامل"):
                    st.code(result_json, language="json")

            except json.JSONDecodeError as e:
                st.error(f"❌ كود JSON غير صالح: {e}")
            except Exception as e:
                st.error(f"❌ خطأ في التحويل: {e}")
                import traceback
                st.code(traceback.format_exc())

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px;">
    🔄 محوّل LP → YouCan | يدعم جميع أقسام Landing Page<br>
    الأنواع المدعومة: row, title, column, link-button, spacer, countdown, express-checkout-form, image
</div>
""", unsafe_allow_html=True)
