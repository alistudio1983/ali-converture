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
                "countdown-si
