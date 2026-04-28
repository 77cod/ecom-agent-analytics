
/**
 * 全局行业状态管理
 */
import { proxy, subscribe } from 'valtio'

// 行业配置类型
export interface IndustryConfig {
  id: string
  name: string
  description: string
  // 资讯搜索关键词
  newsKeywords: string[]
  // 招投标搜索关键词
  biddingKeywords: string[]
  // 研究相关关键词
  researchKeywords: string[]
}

// 预定义的电商品类配置
export const INDUSTRY_CONFIGS: IndustryConfig[] = [
  {
    id: 'fashion',
    name: '服装鞋包',
    description: '防晒衣、连衣裙、运动鞋、箱包等品类运营分析',
    newsKeywords: [
      '防晒衣 市场趋势',
      '女装 爆款',
      '运动鞋 销量',
      '服装 直播带货',
      '鞋包 竞品分析',
      '服饰 达人种草',
    ],
    biddingKeywords: [
      '服装供应链',
      '服饰代工',
      '面料采购',
      '鞋类代工',
    ],
    researchKeywords: ['服装', '鞋包', '防晒衣', '连衣裙', '运动鞋'],
  },
  {
    id: 'beauty',
    name: '美妆个护',
    description: '护肤品、彩妆、洗发水、身体护理等品类运营分析',
    newsKeywords: [
      '护肤品 市场趋势',
      '彩妆 爆款',
      '面膜 销量',
      '美妆 直播带货',
      '精华 竞品分析',
      '个护 达人种草',
    ],
    biddingKeywords: [
      '化妆品代工',
      '护肤品原料',
      '彩妆OEM',
      '个护代工',
    ],
    researchKeywords: ['美妆', '护肤', '彩妆', '面膜', '精华液'],
  },
  {
    id: 'digital',
    name: '数码家电',
    description: '手机、耳机、小家电、智能穿戴等品类运营分析',
    newsKeywords: [
      'TWS耳机 市场趋势',
      '小家电 爆款',
      '智能手表 销量',
      '数码 直播带货',
      '手机配件 竞品分析',
      '家电 达人种草',
    ],
    biddingKeywords: [
      '电子产品代工',
      '小家电OEM',
      '数码配件采购',
    ],
    researchKeywords: ['数码', '家电', '耳机', '智能手表', '小家电'],
  },
  {
    id: 'food',
    name: '食品饮料',
    description: '零食、茶饮、保健品、预制菜等品类运营分析',
    newsKeywords: [
      '零食 市场趋势',
      '茶饮 爆款',
      '保健品 销量',
      '食品 直播带货',
      '预制菜 竞品分析',
      '饮料 达人种草',
    ],
    biddingKeywords: [
      '食品代工',
      '饮料OEM',
      '零食采购',
      '保健品代工',
    ],
    researchKeywords: ['食品', '饮料', '零食', '茶饮', '保健品'],
  },
]

// 行业状态
export interface IndustryState {
  currentIndustryId: string
  industries: IndustryConfig[]
}

// 从 localStorage 读取
const getStoredIndustryId = (): string => {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('selected_industry_id')
    console.log('[industry store] 从 localStorage 读取行业:', stored)
    return stored || 'fashion'
  }
  return 'fashion'
}

// 创建状态
export const industryState = proxy<IndustryState>({
  currentIndustryId: getStoredIndustryId(),
  industries: INDUSTRY_CONFIGS,
})

// 订阅变化，保存到 localStorage
subscribe(industryState, () => {
  if (typeof window !== 'undefined') {
    console.log('[industry store] 保存行业到 localStorage:', industryState.currentIndustryId)
    localStorage.setItem('selected_industry_id', industryState.currentIndustryId)
  }
})

// 获取当前行业配置
export const getCurrentIndustry = (): IndustryConfig => {
  const industry = industryState.industries.find(
    (i) => i.id === industryState.currentIndustryId
  )
  console.log('[industry store] 获取当前行业:', industry?.name)
  return industry || INDUSTRY_CONFIGS[0]
}

// 切换行业
export const setCurrentIndustry = (industryId: string) => {
  console.log('[industry store] 切换行业:', industryId)
  industryState.currentIndustryId = industryId
}

// 获取行业列表（用于选择器）
export const getIndustryOptions = () => {
  return industryState.industries.map((i) => ({
    value: i.id,
    label: i.name,
    description: i.description,
  }))
}
