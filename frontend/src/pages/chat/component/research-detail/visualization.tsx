
import { BarChartOutlined, PictureOutlined } from '@ant-design/icons'
import { useMemo } from 'react'
import ReactECharts from 'echarts-for-react'
import styles from './visualization.module.scss'

interface ChartConfig {
  id: string
  title: string
  subtitle?: string
  type: 'line' | 'bar' | 'pie' | 'horizontal_bar' | 'radar' | 'sankey' | 'wordcloud' | 'graph'
  echarts_option?: Record<string, unknown>
  image_base64?: string  // 支持 matplotlib 生成的图片
}

interface VisualizationProps {
  charts?: ChartConfig[]
}

/** 增强 ECharts 选项：补全交互、防遮挡（不覆盖后端已配好的内容） */
function enhanceEChartsOption(
  option: Record<string, unknown>,
  chartType: string
): Record<string, unknown> {
  const isXY = chartType === 'line' || chartType === 'bar' || chartType === 'horizontal_bar'

  return {
    ...option,
    // tooltip 不超出容器
    tooltip: { confine: true, ...(option.tooltip as Record<string, unknown> || {}) },
    // 工具箱：区域缩放 + 保存图片
    toolbox: {
      show: true,
      feature: {
        ...(isXY ? { dataZoom: { show: true, title: { zoom: '区域缩放', back: '还原' } } } : {}),
        saveAsImage: { show: true, title: '保存图片' },
      },
      right: 10,
      top: -3,
      itemSize: 13,
      ...(option.toolbox as Record<string, unknown> || {}),
    },
    // XY 图表：拖拽/滚轮缩放
    dataZoom: isXY ? (option.dataZoom || [
      { type: 'inside', start: 0, end: 100 },
      { type: 'slider', start: 0, end: 100, height: 18, bottom: 0 },
    ]) : undefined,
    // 饼图：防标签重叠
    ...(chartType === 'pie' ? {
      series: (option.series as any[] || []).map((s: any) => ({
        avoidLabelOverlap: true,
        radius: s.radius || ['40%', '65%'],
        emphasis: {
          scale: true,
          scaleSize: 12,
          focus: 'self',
          ...(s.emphasis || {}),
        },
        label: {
          formatter: (p: any) => p.percent < 5 ? '' : `${p.name}: ${p.percent}%`,
          fontSize: 11,
          ...(s.label || {}),
        },
        ...s,
      })),
    } : {}),
  }
}

export default function Visualization({ charts }: VisualizationProps) {
  console.log(`[Visualization] 渲染，charts 数量: ${charts?.length || 0}`)
  if (charts?.length) {
    charts.forEach((c, i) => {
      console.log(`[Visualization] 图表 ${i+1}: id=${c.id}, title=${c.title}, type=${c.type}, has_echarts=${!!c.echarts_option}, has_image=${!!c.image_base64}`)
    })
  }

  // 增强图表选项，一次性计算
  const enhancedCharts = useMemo(() => {
    return charts?.map((c) => ({
      ...c,
      echarts_option: c.echarts_option
        ? enhanceEChartsOption(c.echarts_option, c.type)
        : undefined,
    }))
  }, [charts])

  if (!enhancedCharts?.length) {
    console.log(`[Visualization] 无图表数据，显示空状态`)
    return (
      <div className={styles.empty}>
        <BarChartOutlined className={styles.emptyIcon} />
        <span>暂无可视化图表</span>
      </div>
    )
  }

  return (
    <div className={styles.grid}>
      {enhancedCharts.map((chart) => (
        <div key={chart.id} className={styles.card}>
          <div className={styles.cardHeader}>
            <h3 className={styles.cardTitle}>{chart.title}</h3>
            {chart.subtitle && <p className={styles.cardSubtitle}>{chart.subtitle}</p>}
          </div>
          <div className={styles.chartContainer}>
            {chart.image_base64 ? (
              // 渲染 matplotlib 生成的 base64 图片
              <div className={styles.imageWrapper}>
                <img
                  src={`data:image/png;base64,${chart.image_base64}`}
                  alt={chart.title}
                  className={styles.chartImage}
                />
              </div>
            ) : chart.echarts_option ? (
              // 渲染 ECharts 图表（增强交互）
              <ReactECharts
                option={chart.echarts_option}
                style={{ height: '100%', width: '100%' }}
                opts={{ renderer: 'canvas', locale: 'ZH' }}
                notMerge={true}
              />
            ) : (
              // 无数据占位
              <div className={styles.noData}>
                <PictureOutlined />
                <span>图表数据加载中...</span>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
