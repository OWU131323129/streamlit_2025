import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("貯金シミュレータ")
st.write("収入と生活費をもとに、貯金達成までの期間を確認できます。")

# 目標金額
target_savings = st.number_input("💰目標貯金額（円）", min_value=0, value=1000000, step=10000)

# 入力
with st.expander("1ヵ月の支出入力"):
    income = st.number_input("月収（手取り・円）", min_value=0, value=200000, step=1000)

    rent = st.number_input("家賃（円）", min_value=0, value=60000, step=1000)

    electricity = st.number_input("電気代（円）", min_value=0, value=7000, step=500)
    elec_reduce = 0
    elec_checked = st.checkbox("電気代を節約する")
    if elec_checked:
        elec_reduce = st.slider("何円減らす？", 0, electricity, 500, step=500)

    water = st.number_input("水道代（円）", min_value=0, value=2500, step=500)
    water_reduce = 0
    water_checked = st.checkbox("水道代を節約する")
    if water_checked:
        water_reduce = st.slider("何円減らす？", 0, water, 500, step=500)

    gas = st.number_input("ガス代（円）", min_value=0, value=3500, step=500)
    gas_reduce = 0
    gas_checked = st.checkbox("ガス代を節約する")
    if gas_checked:
        gas_reduce = st.slider("何円減らす？", 0, gas, 500, step=500)

    food = st.number_input("食費（円）", min_value=0, value=35000, step=1000)
    food_reduce = 0
    food_checked = st.checkbox("食費を節約する")
    if food_checked:
        food_reduce = st.slider("何円減らす？", 0, food, 1000, step=1000)
    
    comm = st.number_input("通信費（円）", min_value=0, value=8000, step=500)
    comm_reduce = 0
    comm_checked = st.checkbox("通信費を節約する")
    if comm_checked:
        comm_reduce = st.slider("何円減らす？", 0, comm, 500, step=500)

    others = st.number_input("その他（衣類・娯楽・交際など）", min_value=0, value=40000, step=1000)
    others_reduce = 0
    others_checked = st.checkbox("その他を節約する")
    if others_checked:
        others_reduce = st.slider("何円減らす？", 0, others, 1000, step=1000)


# 節約前の支出
expense_normal = rent + electricity + water + gas + food + comm + others

# 節約後の支出
electricity_s = electricity - elec_reduce
water_s = water - water_reduce
gas_s = gas  - gas_reduce
food_s = food - food_reduce
comm_s = comm - comm_reduce
others_s = others  - others_reduce
expense_saving = rent + electricity_s + water_s + gas_s + food_s + comm_s + others_s

# 支出の表示
any_checked = any([elec_checked, water_checked, gas_checked, food_checked,comm_checked ,others_checked])
st.markdown(f"### 💸 月間支出合計（節約前）: **{expense_normal}円** 💸")
if any_checked:
    st.markdown(f"### 💸 月間支出合計（節約後）: **{expense_saving}円** 💸")
    with st.expander("詳細"):
        if elec_checked:
            st.write(f"電気代: {electricity}円 →  {electricity_s}円")
        if water_checked:
            st.write(f"水道代: {water}円 →  {water_s}円")
        if gas_checked:
            st.write(f"ガス代: {gas}円 →  {gas_s}円")
        if food_checked:
            st.write(f"食費: {food}円 →  {food_s}円")
        if comm_checked:
            st.write(f"通信費: {comm}円 →  {comm_s}円")
        if others_checked:
            st.write(f"その他: {others}円 →  {others_s}円")


# 節約なし
monthly_savings_normal = income - expense_normal
# 節約あり
monthly_savings_saving = income - expense_saving

if monthly_savings_saving <= 0:
    st.error("この支出だと赤字です！収入を増やすか支出を見直しましょう。")
else:
    # 期間計算
    total_months_normal = int(target_savings / monthly_savings_normal) if monthly_savings_normal > 0 else -1
    total_months_saving = int(target_savings / monthly_savings_saving)

    # 表示
    if monthly_savings_normal > 0:
        y1, m1 = divmod(total_months_normal, 12)
        st.success(f"節約しない場合: **{y1}年{m1}ヶ月** で達成")
    else:
        st.warning("節約しない場合は赤字です。")

    if any_checked:
        y2, m2 = divmod(total_months_saving, 12)
        st.success(f"節約した場合: **{y2}年{m2}ヶ月** で達成")

    # グラフ描画
    st.subheader("貯金推移グラフ")
    months = max(total_months_normal, total_months_saving) + 4
    x = np.arange(months)
    y_normal = x * monthly_savings_normal
    y_saving = x * monthly_savings_saving

    fig, ax = plt.subplots()
    if monthly_savings_normal > 0:
        ax.plot(x, y_normal, label="Baseline", color="red")
    if any_checked:
        ax.plot(x, y_saving, label="With Savings Efforts", color="blue")

    ax.set_xlabel("Month")
    ax.set_ylabel("Savings(JPY)")
    ax.set_title("Saving Growth")
    ax.grid(True)
    ax.legend(prop={"family": "Meiryo"})
    ax.ticklabel_format(style='plain', axis='y')
    ax.axhline(y=target_savings,color='green', linestyle='--')

    st.pyplot(fig)
