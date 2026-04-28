
/**
 * Chart Component - 图表组件
 *
 * 基于 ECharts 的通用图表组件，支持：
 * - 折线图 (Line)
 * - 柱状图 (Bar)
 * - 饼图 (Pie)
 * - 散点图 (Scatter)
 * - 数据表格 (Table)
 */

import { Table } from 'antd'
import { useEffect, useRef, useState } from 'react'
import styles from './chart.module.scss'
import type { ChartConfig, ChartType } from './types'

// 动态加载 ECharts
let echarts: typeof import('echarts') | null = null
let localeRegistered = false

async function loadECharts() {
  if (!echarts) {
    echarts = await import('echarts')
  }
  // 注册中文语言包
  if (!localeRegistered) {
    try {
      const { default: zhLocale } = await import('echarts/i18n/langZH')
      echarts.registerLocale('ZH', zhLocale)
      localeRegistered = true
    } catch {
      // 低版本 echarts 可能没有独立 i18n，尝试从 core 导入
      try {
        echarts.registerLocale('ZH', {})
        localeRegistered = true
      } catch {
        // 忽略，使用默认英文
      }
    }
  }
  return echarts
}

interface ChartProps {
  config: ChartConfig
  width?: string | number
  height?: string | number
  className?: string
}

// 折线图/柱状图/饼图/散点图组件
function EChartsRenderer(props: {
  config: ChartConfig
  width?: string | number
  height?: string | number
}) {
  const { config, width = '100%', height = 400 } = props
  const chartRef = useRef<HTMLDivElement>(null)
  const chartInstance = useRef<ReturnType<typeof echarts.init> | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true

    async function initChart() {
      if (!chartRef.current) return

      try {
        const ec = await loadECharts()

        if (!mounted || !chartRef.current) return

        // 初始化或获取实例
        if (!chartInstance.current) {
          chartInstance.current = ec.init(chartRef.current, undefined, { locale: 'ZH' })
        }

        // 设置配置
        const option = config.echarts_option || buildDefaultOption(config)
        chartInstance.current.setOption(option, { notMerge: true })

        setLoading(false)
      } catch (error) {
        console.error('Failed to initialize chart:', error)
        setLoading(false)
      }
    }

    initChart()

    // 处理窗口大小变化
    const handleResize = () => {
      chartInstance.current?.resize()
    }
    window.addEventListener('resize', handleResize)

    return () => {
      mounted = false
      window.removeEventListener('resize', handleResize)
      chartInstance.current?.dispose()
      chartInstance.current = null
    }
  }, [config])

  return (
    <div className={styles.chartWrapper}>
      {config.title && <div className={styles.chartTitle}>{config.title}</div>}
      <div
        ref={chartRef}
        style={{
          width: typeof width === 'number' ? `${width}px` : width,
          height: typeof height === 'number' ? `${height}px` : height,
        }}
        className={styles.chartContainer}
      />
      {loading && <div className={styles.chartLoading}>加载图表中...</div>}
    </div>
  )
}

// 构建默认配置
function buildDefaultOption(config: ChartConfig) {
  const { type, title, data } = config

  const baseOption = {
    title: {
      text: title,
      left: 'center',
      textStyle: { fontSize: 14 },
    },
    tooltip: {
      trigger: type === 'pie' ? 'item' as const : 'axis' as const,
      confine: true,  // 防止 tooltip 超出容器
    },
    toolbox: {
      show: true,
      feature: {
        // 点击数据点可以区域缩放
        dataZoom: { show: true, title: { zoom: '区域缩放', back: '还原' } },
        // 保存图表为图片
        saveAsImage: { show: true, title: '保存图片' },
      },
      right: 20,
      top: -5,
      itemSize: 14,
    },
    // 区域缩放组件，可通过拖拽底部滑块放大查看数据
    dataZoom: type === 'line' || type === 'bar' ? [
      { type: 'inside', start: 0, end: 100 },
      { type: 'slider', start: 0, end: 100, height: 20, bottom: 0 },
    ] : undefined,
    legend: {
      bottom: 0,
      type: 'scroll',  // 图例过多时可滚动
      textStyle: { fontSize: 11 },
    },
    color: [
      '#5470c6',
      '#91cc75',
      '#fac858',
      '#ee6666',
      '#73c0de',
      '#3ba272',
      '#fc8452',
      '#9a60b4',
    ],
    animation: true,
    animationDuration: 500,
  }

  if (type === 'line' || type === 'bar') {
    return {
      ...baseOption,
      grid: {
        left: '5%',
        right: '5%',
        bottom: type === 'bar' ? '20%' : '18%',
        top: '12%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: data?.xAxis || [],
        axisLabel: {
          rotate: data?.xAxis && data.xAxis.length > 4 ? 30 : 0,  // 长文本旋转防遮挡
          interval: 0,  // 强制显示所有标签
          fontSize: 11,
          overflow: 'truncate',
          width: 80,
        },
        axisTick: { alignWithLabel: data?.xAxis && data.xAxis.length <= 6 },
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: (val: number) => {
            if (val >= 100000000) return (val / 100000000).toFixed(2) + '亿'
            if (val >= 10000) return (val / 10000).toFixed(1) + '万'
            return String(val)
          },
        },
      },
      series:
        data?.series?.map((s) => ({
          name: s.name,
          type,
          data: s.data,
          smooth: type === 'line',
          emphasis: {
            focus: 'series',  // 悬停时高亮整条线
            itemStyle: { borderWidth: 2, borderColor: '#fff' },
          },
          // 数据点标记
          ...(data?.series?.length === 1 || type === 'bar' ? {
            itemStyle: { borderRadius: type === 'bar' ? [4, 4, 0, 0] : undefined },
            label: type === 'bar' ? {
              show: true,
              position: 'top',
              fontSize: 10,
              color: '#666',
            } : undefined,
          } : {}),
        })) || [],
    }
  }

  if (type === 'pie') {
    return {
      ...baseOption,
      legend: {
        ...baseOption.legend,
        bottom: 10,
        type: 'scroll',
        textStyle: { fontSize: 11 },
        pageIconSize: 10,
      },
      series: [
        {
          type: 'pie',
          radius: ['40%', '65%'],  // 环形图，更好的空间利用
          center: ['50%', '45%'],
          data: data?.series?.[0]?.data || [],
          avoidLabelOverlap: true,  // 防止标签重叠
          itemStyle: {
            borderRadius: 4,
            borderColor: '#fff',
            borderWidth: 2,
          },
          emphasis: {
            // 点击/悬停时放大效果
            scale: true,
            scaleSize: 12,
            focus: 'self',
            label: { show: true, fontSize: 14, fontWeight: 'bold' },
            itemStyle: { shadowBlur: 20, shadowColor: 'rgba(0,0,0,0.2)' },
          },
          label: {
            show: true,
            formatter: (p: { name: string; percent: number }) => {
              if (p.percent < 5) return ''  // 占比<5%不显示标签，避免重叠
              return `${p.name}: ${p.percent}%`
            },
            fontSize: 11,
            overflow: 'truncate',
          },
          labelLine: {
            show: true,
            length: 20,
            length2: 25,
          },
        },
      ],
    }
  }

  if (type === 'scatter') {
    return {
      ...baseOption,
      grid: {
        left: '5%',
        right: '5%',
        bottom: '15%',
        top: '12%',
        containLabel: true,
      },
      xAxis: {
        type: 'value',
        axisLabel: { fontSize: 11 },
      },
      yAxis: {
        type: 'value',
        axisLabel: { fontSize: 11 },
      },
      series: [
        {
          type: 'scatter',
          data: data?.series?.[0]?.data || [],
          symbolSize: 12,
          emphasis: {
            scale: true,
            scaleSize: 2,
            itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' },
          },
        },
      ],
    }
  }

  return baseOption
}

// 表格组件
function TableRenderer(props: { config: ChartConfig }) {
  const { config } = props

  const columns =
    config.columns?.map((col) => ({
      title: col.label,
      dataIndex: col.key,
      key: col.key,
    })) || []

  const dataSource =
    (config.data as unknown as Record<string, unknown>[]) || []

  return (
    <div className={styles.tableWrapper}>
      {config.title && <div className={styles.chartTitle}>{config.title}</div>}
      <Table
        columns={columns}
        dataSource={dataSource.map((item, index) => ({
          ...item,
          key: index,
        }))}
        pagination={
          config.pagination
            ? { pageSize: config.pageSize || 10 }
            : false
        }
        size="small"
        scroll={{ x: 'max-content' }}
      />
    </div>
  )
}

// 主组件
export function Chart(props: ChartProps) {
  const { config, width, height, className } = props

  if (!config) {
    return null
  }

  const chartType = config.type as ChartType

  return (
    <div className={`${styles.chart} ${className || ''}`}>
      {chartType === 'table' ? (
        <TableRenderer config={config} />
      ) : (
        <EChartsRenderer config={config} width={width} height={height} />
      )}
    </div>
  )
}

// 数据洞察展示组件
export function DataInsights(props: {
  insights: string[]
  className?: string
}) {
  const { insights, className } = props

  if (!insights || insights.length === 0) {
    return null
  }

  return (
    <div className={`${styles.insights} ${className || ''}`}>
      <div className={styles.insightsTitle}>数据洞察</div>
      <ul className={styles.insightsList}>
        {insights.map((insight, index) => (
          <li key={index} className={styles.insightItem}>
            {insight}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Chart
export type { ChartConfig, ChartType, DataInsight } from './types'
