import streamlit as st
import pandas as pd
import altair as alt
import base64
import time
import streamlit.components.v1 as components

import urllib.parse

st.set_page_config(
    page_title="Then vs Now! クイズ　『ワシの若い頃は…』",
    page_icon="text_versus_vs.png",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Report a bug': "https://masayoshi.work/",
        'About': "Then vs Now! クイズ　『ワシの若い頃は…』"
    }
)

# st.markdown()内のファイル名は変換されないので、ファイル名を手動で変換
def get_base64_img(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{encoded}"

# CSSで画像の幅を調整（スマホ対応）
st.markdown("""
<style>
.chat-row {
    display: flex;
    align-items: center;
    margin-bottom: 1.5em;
    flex-wrap: wrap;
}
.chat-row img {
    width: 80px;
    height: auto;
    margin-right: 1em;
    border-radius: 8px;
}
.chat-row .dialogue {
    font-size: 1.1em;
    max-width: 80%;
}
</style>
""", unsafe_allow_html=True)

# streamlit cloud で公開するURL
siteUrl = "";

# 考えているフリ
sleepTime = 1.5

# 犯罪白書からデータを抜粋したcsvファイルを用意して読み込む
csvFileName = "crime.csv"
df = pd.read_csv(csvFileName)
df.sort_values(by="西暦",inplace=True)

# DEBUG用
# st.dataframe(df)

# データ型を数字に変換
df["西暦"] = pd.to_numeric(df["西暦"],errors="coerce")
df["件数"] = pd.to_numeric(df["件数"],errors="coerce")

# 西暦の一覧を取得（重複排除＆昇順ソート）
years = sorted(df["西暦"].dropna().unique())

# 最新のデータがある年
max_year = df["西暦"].max()

# タイトル表示
st.header("Then vs Now!")
st.header("クイズ　『ワシの若い頃は…』",divider='red')
st.image("titleImage.png",use_container_width=True)

with st.expander("注意・免責事項",icon="⚠️"):
    st.write("""
        本Webアプリはジョークアプリです。特定の年代、年齢の方々を侮辱する意図はありません。
        情報の正確性や完全性に努めていますが、なんら保証するものではありません。
        
        ご利用によって生じたいかなる損害・不利益についても、開発者は一切責任を負いません。
        ご理解のうえ、お楽しみください。
    """)

st.divider()

# 入力フォーム
st.markdown("""
#### 問題
""")

# 最小年・最大年をスライダーに設定
selected_year = st.slider("スライドして年数を変更", int(years[0]), int(years[-2]),value=int(pd.Series(years).median()) )
questionText = f"刑法犯が多いのは {selected_year} 年と { max_year } 年 のどっち？"
st.subheader(questionText,divider="gray")

st.markdown(f"""
<div class="chat-row">
    <br><br>
    <img src="{get_base64_img("ojiisan03_smile.png")}">
    <div class="dialogue">ワシの若い頃は、夜に玄関の鍵なんてかけなかったもんじゃ。<br> {selected_year} 年が少ないに決まっとろうて！<br>最近の若いモンは…</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="chat-row">
    <img src="{get_base64_img("suit_man_smile.png")}">
    <div class="dialogue">どう考えてもタワゴトです。本当にありがとうございます。<br> {max_year} 年の方が少ないに決まってます！！</div>
</div>
""", unsafe_allow_html=True)

options = ["お爺さんが正しい！","若者が正しい！","実は同じでは？"]

judgment=st.pills(" ",options,selection_mode="single")

if judgment:
    if st.button("判定はいかに？", type="primary"):
        st.subheader(f" ",divider="gray")

        # 時間稼ぎ。ドラムロール的な
        with st.spinner("Wait for it...", show_time=True):
            time.sleep(sleepTime)

        # スクロール用アンカー（HTMLのidを埋め込む）
        st.markdown('<div id="result"></div>', unsafe_allow_html=True)

        # 演算
        oldManCount = int(df.loc[df["西暦"] == selected_year,"件数"].iloc[0])
        youngManCount = int(df.loc[df["西暦"] == max_year,"件数"].iloc[0])

        if oldManCount == youngManCount:
            result = "引き分け"
            st.image('draw.png')
            if judgment == "実は同じでは？":
                your_result = "あたり"
            else:
                your_result = "はずれ"
        elif oldManCount < youngManCount:
            result = "お爺さんの勝利！"
            st.image('ojiisan05_win.png')
            if judgment == "お爺さんが正しい！":
                your_result = "あたり"
            else:
                your_result = "はずれ"
        elif oldManCount > youngManCount:
            result = "若者の勝利！"
            st.image('suit_man_win.png')
            if judgment == "若者が正しい！":
                your_result = "あたり"
            else:
                your_result = "はずれ"
        else:
            result = "…審議中…"
            your_result = "…審議中…"
            st.image('draw.png')

        # 結果出力
        st.subheader("判定 『" + result + "』 あなたの予想は 『" + your_result + "』",divider="green")
        if result == "若者の勝利！":
            st.markdown(f"""
            <div class="chat-row">
                <img src="{get_base64_img("suit_man_smile.png")}">
                <div class="dialogue">{max_year} 年の刑法犯 認知件数は { youngManCount } 件<br>{selected_year} 年は {oldManCount} 件です！</div>
            </div>
            """, unsafe_allow_html=True)
        elif result == "お爺さんの勝利！":
            st.markdown(f"""
            <div class="chat-row">
                <img src="{get_base64_img("ojiisan03_smile.png")}">
                <div class="dialogue">{selected_year} 年の刑法犯 認知件数は {oldManCount} 件<br> {max_year} 年は { youngManCount } 件じゃ</div>
            </div>
            """, unsafe_allow_html=True)
        elif result == "引き分け":
            st.markdown(f"""
            <div class="chat-row">
                <img src="{get_base64_img("draw.png")}">
                <div class="dialogue">{selected_year} 年の刑法犯認知件数は {oldManCount} 件<br> {max_year} 年は { youngManCount } 件</div>
            </div>
            """, unsafe_allow_html=True)

        # twitter 出力
        # スクロール用アンカー（HTMLのidを埋め込む）
        st.markdown('<div id="twitter"></div>', unsafe_allow_html=True)
        #tweet用テキスト
        tweet_text = f"""#ワシの若い頃は #ThenVsNow
{questionText}
私の予想は『{your_result}』
"""
        tweet_footer = f"""👇クイズはこちら
{siteUrl}
"""
        # tweet_textの内容を140文字に制限
        tweet_text = tweet_text[:138+len(tweet_footer)] + "…" + tweet_footer
        # URLエンコード
        tweet_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet_text)

        st.link_button(f"📝 結果をXに投稿する", tweet_url, type="secondary")


        # 刑法犯発生件数の推移をプロット
        with st.expander("参考資料",expanded=False):
            st.markdown("""

                ### データは法務省サイトより引用いたしました
                - 犯罪白書 https://hakusyo1.moj.go.jp/jp/nendo_nfm.html
                    - 刑法犯 認知件数を利用させて頂きました。
                - 刑法犯発生件数の推移
            """)
            chart = alt.Chart(df).mark_line().encode(
                x=alt.X("西暦:Q", axis=alt.Axis(format="d", title="西暦")),  # カンマ無し
                y=alt.Y("件数:Q", title="件数"),
                tooltip=["西暦", "件数"]
            ).properties(
                title="",
                width=600,
                height=400
            )
            st.altair_chart(chart, use_container_width=True)

        # JavaScriptでその位置にスクロール
        components.html("""
            <script>
                const element = window.parent.document.querySelector('div[id="result"]');
                if (element) {
                    element.scrollIntoView({behavior: "smooth"});
                }
            </script>
        """, height=0)
