# 準備
1. [SONY MESH](https://meshprj.com/jp/)の用意．  
2. 始めに以下のコマンドを実行し，ライブラリをインストール．
    ```cmd
    pip install bleak
    ```
3. `mesh-controller.py`を実行し，以下の変数値を変更．`mesh-allocation-template.csv`を参照し，使用したいブロックの値(上から数えた際のインデックス)に変更．
    ```python
    class Mesh:
        device_num = 0
    ```  

# 参考
- [サンプルプログラム](https://developer.meshprj.com/hc/ja/articles/9164308204313-Python#h_01GBRQZG0TQCSR53E7T2FAQ3PD)  
- [Button](https://developer.meshprj.com/hc/ja/articles/8286402535577)  
- [Move](https://developer.meshprj.com/hc/ja/articles/8286418941977)  
- [Motion](https://developer.meshprj.com/hc/ja/articles/8286408492057)  
- [Brightness](https://developer.meshprj.com/hc/ja/articles/8286460847897)  
- [Temperature](https://developer.meshprj.com/hc/ja/articles/8286425847961)  
- [LED](https://developer.meshprj.com/hc/ja/articles/9231602345497)  
