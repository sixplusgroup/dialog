# 预处理
rm -rf TODO/wav_new/
python3.8 convert_wavs.py TODO/wav/ TODO/wav_new/ # 必须加斜杠 不然不知道为什么会理解成.wav和.wav_new
python3.8 delete_less_than_one_mbyte.py

# 案例生成
python3.8 main.py

# 客服评价
python3.8 staff_evaluation.py