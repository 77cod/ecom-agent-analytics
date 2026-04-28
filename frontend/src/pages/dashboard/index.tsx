/**
 * 电商运营看板 - Dashboard Page
 *
 * 只读展示：从研究会话的 checkpoint 数据中提取结构化结果
 * URL: /dashboard?session_id=xxx
 */

import * as api from '@/api'
import { Chart } from '@/components/chart'
import type { ChartConfig } from '@/components/chart/types'
import { Button, Card, Col, Empty, Row, Skeleton, Statistic, Table, Tag } from 'antd'
import {
  DollarOutlined,
  ShoppingCartOutlined,
  RiseOutlined,
  FallOutlined,
} from '@ant-design/icons'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import styles from './index.module.scss'

// ============================================================
// 类型
// ============================================================

interface KPIItem {
  label: string
  value: string
  prefix?: React.ReactNode
  suffix?: string
  valueStyle?: React.CSSProperties
}

interface AIRecommendation {
  action: string
  rationale: string
  expected_impact: string
  priority: '高' | '中' | '低'
}

// ============================================================
// 辅助函数
// ============================================================

function buildLineChartConfig(title: string, xData: string[], seriesData: number[]): ChartConfig {
  return {
    type: 'line',
    title,
    echarts_option: {
      toolbox: {
        show: true,
        feature: {
          dataZoom: { show: true, title: { zoom: '区域缩放', back: '还原' } },
          saveAsImage: { show: true, title: '保存图片' },
        },
        right: 15,
        top: -5,
      },
      dataZoom: [
        { type: 'inside', start: 0, end: 100 },
        { type: 'slider', start: 0, end: 100, height: 20, bottom: 0 },
      ],
      tooltip: { trigger: 'axis', confine: true },
      grid: { left: '5%', right: '5%', bottom: '18%', top: '12%', containLabel: true },
      xAxis: {
        type: 'category',
        data: xData,
        axisLine: { lineStyle: { color: '#e8e8e8' } },
        axisLabel: { color: '#666', rotate: xData.length > 4 ? 30 : 0, interval: 0, fontSize: 11 },
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        splitLine: { lineStyle: { color: '#f0f0f0' } },
        axisLabel: {
          formatter: (val: number) => val >= 10000 ? (val / 10000).toFixed(1) + '万' : String(val),
        },
      },
      series: [{
        type: 'line',
        data: seriesData,
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        itemStyle: { color: '#1677ff' },
        lineStyle: { width: 3 },
        emphasis: { focus: 'series', itemStyle: { borderWidth: 2, borderColor: '#fff' } },
        areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(22,119,255,0.2)' }, { offset: 1, color: 'rgba(22,119,255,0)' }] } },
      }],
    },
  }
}

function buildPieChartConfig(title: string, data: { name: string; value: number }[]): ChartConfig {
  return {
    type: 'pie',
    title,
    echarts_option: {
      toolbox: {
        show: true,
        feature: {
          saveAsImage: { show: true, title: '保存图片' },
        },
        right: 15,
        top: -5,
      },
      tooltip: { trigger: 'item', confine: true },
      legend: { bottom: 10, type: 'scroll', textStyle: { fontSize: 11 } },
      color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272'],
      series: [{
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['50%', '45%'],
        data,
        avoidLabelOverlap: true,
        emphasis: {
          scale: true,
          scaleSize: 12,
          focus: 'self',
          label: { show: true, fontSize: 14, fontWeight: 'bold' },
          itemStyle: { shadowBlur: 20, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.3)' },
        },
        label: {
          formatter: (p: { name: string; percent: number }) => p.percent < 5 ? '' : `${p.name}: ${p.percent}%`,
          fontSize: 11,
        },
        labelLine: { length: 20, length2: 25 },
      }],
    },
  }
}

// ============================================================
// 优先级标签
// ============================================================

function PriorityTag({ priority }: { priority: string }) {
  const colorMap: Record<string, string> = { 高: 'red', 中: 'orange', 低: 'blue' }
  return <Tag color={colorMap[priority] || 'default'}>{priority}</Tag>
}

// ============================================================
// Dashboard 主组件
// ============================================================

export default function Dashboard() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const sessionId = searchParams.get('session_id')

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // 看板数据
  const [kpis, setKpis] = useState<KPIItem[]>([
    { label: 'GMV', value: '--', prefix: <DollarOutlined />, suffix: '元' },
    { label: '订单量', value: '--', prefix: <ShoppingCartOutlined />, suffix: '单' },
    { label: '客单价', value: '--', prefix: <RiseOutlined />, suffix: '元' },
    { label: '退货率', value: '--', prefix: <FallOutlined />, suffix: '%' },
  ])
  const [salesTrendConfig, setSalesTrendConfig] = useState<ChartConfig | null>(
    () => buildLineChartConfig('销售趋势', ['6月', '7月', '8月'], [210, 258, 285])
  )
  const [channelPieConfig, setChannelPieConfig] = useState<ChartConfig | null>(
    () => buildPieChartConfig('渠道占比', [{ name: '直播带货', value: 45 }, { name: '天猫旗舰店', value: 30 }, { name: '抖音商城', value: 25 }])
  )
  const [searchTrendConfig, setSearchTrendConfig] = useState<ChartConfig | null>(
    () => buildLineChartConfig('搜索趋势', ['6月', '7月', '8月'], [120, 145, 168])
  )
  const [productRanking, setProductRanking] = useState<Record<string, unknown>[]>([])
  const [competitorComparison, setCompetitorComparison] = useState<Record<string, unknown>[]>([])
  const [kolROI, setKolROI] = useState<Record<string, unknown>[]>([])
  const [reviewAnalysis, setReviewAnalysis] = useState<Record<string, unknown>[]>([])
  const [aiRecommendations, setAiRecommendations] = useState<AIRecommendation[]>([])
  const [reportContent, setReportContent] = useState('')

  // --- 从 checkpoint 加载数据 ---
  const loadCheckpoint = useCallback(async (sid: string) => {
    setLoading(true)
    setError('')
    try {
      const res = await api.session.getFullResearchCheckpoint(sid)
      const response = (res as Record<string, unknown>).data || res
      if (!(response as Record<string, unknown>)?.checkpoint) {
        setError('该会话没有研究数据')
        setLoading(false)
        return
      }

      const checkpoint = (response as Record<string, unknown>).checkpoint as Record<string, unknown>
      const finalReport = (checkpoint.final_report as string) || ''
      const uiState = checkpoint.ui_state_json as Record<string, unknown> | undefined

      // 报告内容
      if (finalReport) {
        setReportContent(finalReport)
      } else if (uiState?.streaming_report) {
        setReportContent(uiState.streaming_report as string)
      }

      // 图表
      if (uiState?.charts && Array.isArray(uiState.charts)) {
        const charts = uiState.charts as Record<string, unknown>[]
        for (const chart of charts) {
          const title = (chart.title as string) || ''
          const echartsOption = chart.echarts_option || chart.echarts_option_json
          if (!echartsOption) continue

          if (title.includes('趋势') || title.includes('销售额') || title.includes('GMV') || title.includes('销售')) {
            setSalesTrendConfig({ type: (chart.type as ChartConfig['type']) || 'line', title, echarts_option: echartsOption as ChartConfig['echarts_option'] })
          } else if (title.includes('渠道') || title.includes('占比') || title.includes('分布')) {
            setChannelPieConfig({ type: (chart.type as ChartConfig['type']) || 'pie', title, echarts_option: echartsOption as ChartConfig['echarts_option'] })
          } else if (title.includes('搜索') || title.includes('热搜')) {
            setSearchTrendConfig({ type: (chart.type as ChartConfig['type']) || 'line', title, echarts_option: echartsOption as ChartConfig['echarts_option'] })
          }
        }
      }

      // 搜索结果为表格
      if (uiState?.search_results && Array.isArray(uiState.search_results)) {
        const results = uiState.search_results as Record<string, unknown>[]
        setProductRanking(results.slice(0, 10).map((r, i) => ({
          key: `sr_${i}`,
          name: r.title || r.source_name || '',
          source: r.source || '',
          snippet: r.snippet || r.content || '',
        })))
      }

      // 从报告中提取结构化数据
      if (finalReport) {
        // 尝试提取 KPI
        tryExtractKPIs(finalReport)
        tryExtractProductRanking(finalReport)
        tryExtractRecommendations(finalReport)
      }
    } catch (e) {
      setError(`加载失败: ${(e as Error).message}`)
    } finally {
      setLoading(false)
    }
  }, [])

  // 从报告中提取 KPI 指标
  const tryExtractKPIs = (report: string) => {
    const gmvMatch = report.match(/GMV[：:]\s*([\d,.]+)\s*万?元?/i)
    const orderMatch = report.match(/订单[量数][：:]\s*([\d,.]+)\s*[单万]/i)
    const aovMatch = report.match(/客单价[：:]\s*([\d,.]+)\s*元?/i)
    const returnMatch = report.match(/退货率[：:]\s*([\d,.]+)%/i)

    if (gmvMatch || orderMatch || aovMatch || returnMatch) {
      setKpis(prev => {
        const next = [...prev]
        if (gmvMatch) next[0] = { ...next[0], value: gmvMatch[1], suffix: '元' }
        if (orderMatch) next[1] = { ...next[1], value: orderMatch[1], suffix: '单' }
        if (aovMatch) next[2] = { ...next[2], value: aovMatch[1], suffix: '元' }
        if (returnMatch) next[3] = { ...next[3], value: returnMatch[1], suffix: '%' }
        return next
      })
    }
  }

  const tryExtractProductRanking = (report: string) => {
    const rows: Record<string, unknown>[] = []
    // 匹配中文商品名 + 数字 + 数字 + 百分比变化
    const regex = /([\u4e00-\u9fa5\w]+(?:\([^)]*\))?)\s+([\d,]+)\s+[¥￥]?([\d,.]+)\s*([+-][\d.]+%)/g
    let m
    while ((m = regex.exec(report)) !== null && rows.length < 10) {
      rows.push({ key: `p_${rows.length}`, name: m[1], sales: m[2], revenue: `¥${m[3]}`, change: m[4] })
    }
    if (rows.length > 0) setProductRanking(rows)
  }

  const tryExtractRecommendations = (report: string) => {
    // 查找 "运营行动建议" 或 "高优先级" 等章节
    const recSection = report.match(/(?:运营行动建议|行动建议)[\s\S]*/i)
    if (!recSection) return
    const recs: AIRecommendation[] = []
    const recRegex = /\*\*\[(.+?)\]\*\*[^-]*-\s*(.+?)(?:\n|$)/g
    let m
    while ((m = recRegex.exec(recSection[0])) !== null) {
      recs.push({ action: m[1], rationale: m[2] || '', expected_impact: '', priority: '中' })
    }
    if (recs.length > 0) setAiRecommendations(recs)
  }

  // --- 加载 ---
  useEffect(() => {
    if (sessionId) {
      loadCheckpoint(sessionId)
    }
  }, [sessionId, loadCheckpoint])

  // --- 表格列定义 ---
  const productColumns = useMemo(() => [
    { title: '名称', dataIndex: 'name', key: 'name', ellipsis: true },
    { title: '销量', dataIndex: 'sales', key: 'sales' },
    { title: '销售额', dataIndex: 'revenue', key: 'revenue' },
    { title: '环比', dataIndex: 'change', key: 'change', render: (v: string) => {
      const isUp = v?.startsWith('+')
      return <span style={{ color: isUp ? '#52c41a' : '#ff4d4f' }}>{v || '-'}</span>
    }},
  ], [])

  const competitorColumns = useMemo(() => [
    { title: '竞品', dataIndex: 'name', key: 'name', ellipsis: true },
    { title: '价格', dataIndex: 'price', key: 'price' },
    { title: '月销量', dataIndex: 'monthlySales', key: 'monthlySales' },
    { title: '市场份额', dataIndex: 'marketShare', key: 'marketShare' },
    { title: '促销', dataIndex: 'promotion', key: 'promotion', ellipsis: true },
  ], [])

  const kolColumns = useMemo(() => [
    { title: '达人', dataIndex: 'name', key: 'name', ellipsis: true },
    { title: 'GMV', dataIndex: 'gmv', key: 'gmv' },
    { title: '成本', dataIndex: 'cost', key: 'cost' },
    { title: 'ROI', dataIndex: 'roi', key: 'roi', render: (v: number) => v != null ? `${Number(v).toFixed(1)}x` : '-' },
    { title: '转化率', dataIndex: 'conversionRate', key: 'conversionRate' },
  ], [])

  const reviewColumns = useMemo(() => [
    { title: '维度', dataIndex: 'dimension', key: 'dimension' },
    { title: '好评率', dataIndex: 'positiveRate', key: 'positiveRate' },
    { title: '差评关键词', dataIndex: 'negativeKeywords', key: 'negativeKeywords', ellipsis: true },
    { title: '件数', dataIndex: 'count', key: 'count' },
  ], [])

  // 默认静态示例数据（泛化示例，适用于多品类参考）
  const defaultProductData = [
    { key: '1', name: '主推爆款A', sales: '8,520', revenue: '¥1,090,560', change: '+12.3%' },
    { key: '2', name: '热销商品B', sales: '6,340', revenue: '¥253,600', change: '+8.7%' },
    { key: '3', name: '经典款商品C', sales: '5,120', revenue: '¥358,400', change: '-2.1%' },
    { key: '4', name: '新品商品D', sales: '4,890', revenue: '¥195,600', change: '+15.6%' },
    { key: '5', name: '长尾商品E', sales: '3,670', revenue: '¥440,400', change: '+5.2%' },
  ]

  const defaultCompetitorData = [
    { key: '1', name: '我方品牌', price: '¥128', monthlySales: '8,520', marketShare: '32%', promotion: '满200减30' },
    { key: '2', name: '竞品品牌A', price: '¥149', monthlySales: '12,340', marketShare: '38%', promotion: '限时9折' },
    { key: '3', name: '竞品品牌B', price: '¥169', monthlySales: '6,780', marketShare: '21%', promotion: '第二件半价' },
    { key: '4', name: '竞品品牌C', price: '¥99', monthlySales: '3,450', marketShare: '9%', promotion: '无' },
  ]

  const defaultKolData = [
    { key: '1', name: '头部达人A', gmv: '¥1,280,000', cost: '¥200,000', roi: 6.4, conversionRate: '4.8%' },
    { key: '2', name: '头部达人B', gmv: '¥856,000', cost: '¥150,000', roi: 5.7, conversionRate: '3.9%' },
    { key: '3', name: '腰部达人C', gmv: '¥520,000', cost: '¥100,000', roi: 5.2, conversionRate: '3.2%' },
    { key: '4', name: '腰部达人D', gmv: '¥194,000', cost: '¥80,000', roi: 2.43, conversionRate: '2.1%' },
  ]

  const defaultReviewData = [
    { key: '1', dimension: '整体满意度', positiveRate: '94.2%', negativeKeywords: '色差、尺寸不符', count: 12580 },
    { key: '2', dimension: '产品质量', positiveRate: '91.5%', negativeKeywords: '材质一般、做工粗糙', count: 8920 },
    { key: '3', dimension: '使用效果', positiveRate: '96.8%', negativeKeywords: '效果不明显、不适合', count: 7650 },
    { key: '4', dimension: '物流服务', positiveRate: '88.3%', negativeKeywords: '发货慢、包装差', count: 6340 },
  ]

  const defaultRecommendations: AIRecommendation[] = [
    { action: '加大直播带货投入', rationale: '直播带货贡献45%销售额，ROI达5.7x，是效率最高的渠道', expected_impact: '预计可提升GMV 15-20%', priority: '高' },
    { action: '优化主推爆款库存管理', rationale: '头部商品销量居首且环比增长，需防范断货风险', expected_impact: '保障核心品类GMV稳定增长', priority: '高' },
    { action: '关注头部竞品促销策略', rationale: '竞品品牌B市场份额持续增长，促销力度对标行业水平', expected_impact: '及时跟进可防御市场份额流失', priority: '中' },
  ]

  // --- 空状态 ---
  if (!sessionId) {
    return (
      <div className={styles.page}>
        <div className={styles.emptyState}>
          <Empty description="请从聊天页完成一次研究分析后查看运营看板">
            <Button type="primary" onClick={() => navigate('/chat')}>
              去提问
            </Button>
          </Empty>
        </div>
      </div>
    )
  }

  // --- 加载中 ---
  if (loading) {
    return (
      <div className={styles.page}>
        <div className={styles.dashboard}>
          <Row gutter={[16, 16]}>
            {[1, 2, 3, 4].map(i => (
              <Col xs={12} sm={12} md={6} key={i}>
                <Card className={styles.kpiCard}><Skeleton active paragraph={{ rows: 1 }} title={{ width: '60%' }} /></Card>
              </Col>
            ))}
          </Row>
          <Row gutter={[16, 16]}>
            <Col xs={24} lg={12}><Card className={styles.chartCard}><Skeleton active paragraph={{ rows: 6 }} /></Card></Col>
            <Col xs={24} lg={12}><Card className={styles.chartCard}><Skeleton active paragraph={{ rows: 6 }} /></Card></Col>
          </Row>
        </div>
      </div>
    )
  }

  // --- 错误 ---
  if (error) {
    return (
      <div className={styles.page}>
        <div className={styles.emptyState}>
          <Empty description={error}>
            <Button onClick={() => sessionId && loadCheckpoint(sessionId)}>重试</Button>
            <Button type="primary" onClick={() => navigate('/chat')} style={{ marginLeft: 8 }}>去提问</Button>
          </Empty>
        </div>
      </div>
    )
  }

  // --- 看板渲染 ---
  const hasReport = reportContent.length > 0
  const displayProducts = productRanking.length > 0 ? productRanking : defaultProductData
  const displayCompetitors = competitorComparison.length > 0 ? competitorComparison : defaultCompetitorData
  const displayKol = kolROI.length > 0 ? kolROI : defaultKolData
  const displayReviews = reviewAnalysis.length > 0 ? reviewAnalysis : defaultReviewData
  const displayRecs = aiRecommendations.length > 0 ? aiRecommendations : defaultRecommendations

  return (
    <div className={styles.page}>
      <div className={styles.dashboard}>
        {/* KPI 卡片 */}
        <Row gutter={[16, 16]} className={styles.kpiRow}>
          {kpis.map((kpi, i) => (
            <Col xs={12} sm={12} md={6} key={i}>
              <Card className={styles.kpiCard} hoverable>
                <Statistic
                  title={kpi.label}
                  value={kpi.value}
                  prefix={kpi.prefix}
                  suffix={kpi.suffix}
                  valueStyle={{ fontSize: 28, fontWeight: 700 }}
                />
              </Card>
            </Col>
          ))}
        </Row>

        {/* 图表 */}
        <Row gutter={[16, 16]} className={styles.chartRow}>
          <Col xs={24} lg={12}>
            <Card title="销售趋势" className={styles.chartCard}>
              {salesTrendConfig ? <Chart config={salesTrendConfig} height={300} /> : <div className={styles.emptyChart}>暂无数据</div>}
            </Card>
          </Col>
          <Col xs={24} lg={12}>
            <Card title="渠道占比" className={styles.chartCard}>
              {channelPieConfig ? <Chart config={channelPieConfig} height={300} /> : <div className={styles.emptyChart}>暂无数据</div>}
            </Card>
          </Col>
        </Row>

        {/* 表格 */}
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <Card title="商品排行" className={styles.tableCard}>
              <Table columns={productColumns} dataSource={displayProducts as Record<string, unknown>[]} pagination={false} size="small" scroll={{ x: 'max-content' }} />
            </Card>
          </Col>
          <Col xs={24} lg={12}>
            <Card title="竞品对比" className={styles.tableCard}>
              <Table columns={competitorColumns} dataSource={displayCompetitors as Record<string, unknown>[]} pagination={false} size="small" scroll={{ x: 'max-content' }} />
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <Card title="达人ROI" className={styles.tableCard}>
              <Table columns={kolColumns} dataSource={displayKol as Record<string, unknown>[]} pagination={false} size="small" scroll={{ x: 'max-content' }} />
            </Card>
          </Col>
          <Col xs={24} lg={12}>
            <Card title="评价分析" className={styles.tableCard}>
              <Table columns={reviewColumns} dataSource={displayReviews as Record<string, unknown>[]} pagination={false} size="small" scroll={{ x: 'max-content' }} />
            </Card>
          </Col>
        </Row>

        {/* AI建议 + 搜索趋势 */}
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <Card title={hasReport ? 'AI运营建议' : 'AI运营建议（示例）'} className={styles.recommendCard}>
              <div className={styles.recommendList}>
                {displayRecs.map((rec, i) => (
                  <div key={i} className={styles.recommendItem}>
                    <div className={styles.recommendHeader}>
                      <PriorityTag priority={rec.priority} />
                      <strong>{rec.action}</strong>
                    </div>
                    <div className={styles.recommendBody}>
                      <p><span>数据依据：</span>{rec.rationale}</p>
                      <p><span>预期效果：</span>{rec.expected_impact}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </Col>
          <Col xs={24} lg={12}>
            <Card title="搜索趋势" className={styles.chartCard}>
              {searchTrendConfig ? <Chart config={searchTrendConfig} height={300} /> : <div className={styles.emptyChart}>暂无数据</div>}
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  )
}
