# openmv卡尔曼滤波多目标追踪
>卡尔曼滤波的作用是在短暂丢失，遮掩，两个目标重合的情况下保持对物体的追踪。kalman_example.py给出了一个简单的示例，对一个圆周运动和一个不动的点进行追踪，两个点每转一周会有短暂时间的重合。但最终我发现，其对art用处不大，因为art对传统图像算法的优化太差了，导致帧率较低。对普通的openmv可能用处较大。当然，也可将其应用到其它地方，只要将openmv_numpy的调用改为对numpy的调用即可。

[测试视频](https://www.bilibili.com/video/BV1Bd4y1672d/?spm_id_from=333.999.0.0&vd_source=cc02d853015d7ea2c00217e93ecf9751)。

## 使用方法
首先要初始化$A,H,Q,R$矩阵，建立一个Tracker_Manager()，其作用是管理追踪器。然后将每帧图像的目标用math方法进行匹配，之后用update方法进行更新。最后可以用get_motion_trail_pre获得目标的ID和轨迹。

```python
Manager = Tracker_Manager()#定义一个管理器

Manager.match(x,y,A,H_k,Q,R)#进行匹配

Manager.update()#更新管理器

Manager.get_motion_trail_pre()#获取预测坐标轨迹

Manager.get_positions()#获取后验坐标

Manager.get_motion_trail_measure()#获取测量坐标轨迹

```
