# 代码说明

- 主函数

  angle_estimation，主要进程在process方法内，多线程吊用process处理图片对

- 参数

  默认参数设置在option_parser，包含调用mediapipe的参数

  额外设置在angle_estimation开头，包含输入/输出地址，取样半径，关键点组。其中关键点组是写死的，改动时需要配合调用处改动，其中tri_kpt_idx为计算法向量的三角形参考点，all_kpt_idx为掌心关键点

- 方法

  关于图片的方法在paired_image，其中sample_v1为取样方法，根据关键点选取不同改动

- 可视化

  vis生成输出图片

- 检验

  examination，检验输入图片是否符合格式，这里包含了id（文件名）的确认

# 待改动

- 目前计算法向量夹角的方法要求手腕-指尖一线需要保持竖直，需要代入平面法向量参数进行修改
- 静脉提取的代码在Palm_Vein目录下，可以进一步根据掌静脉位置减少掌纹带来的误差

