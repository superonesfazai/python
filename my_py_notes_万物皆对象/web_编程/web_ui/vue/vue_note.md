# vue
Vue.js是一套构建用户界面的渐进式框架。

Vue 只关注视图层， 采用自底向上增量开发的设计。

Vue 的目标是通过尽可能简单的 API 实现响应的数据绑定和组合的视图组件。

Vue 学习起来非常简单，本教程基于 Vue 2.1.8 版本测试。

```html
<!-- 开发版，包括有用的控制台警告 --> 
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
<!-- 生产版本，针对大小和速度进行了优化 --> 
<script src="https://cdn.jsdelivr.net/npm/vue"></script>
```

## 指令
v-bind: 您看到的属性称为指令。指令带有前缀，v-表示它们是Vue提供的特殊属性，正如您可能已经猜到的那样，它们对呈现的DOM应用特殊的反应行为。