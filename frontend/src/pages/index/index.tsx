
import IconBg from '@/assets/index/bg.png'
import IconSearch from '@/assets/index/search.svg'
import { Input, message } from 'antd'
import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { INDUSTRY_CONFIGS, setCurrentIndustry } from '@/store/industry'
import styles from './index.module.scss'

// 品类卡片颜色配置
const INDUSTRY_COLORS: Record<string, { color: string; bgColor: string }> = {
  fashion: { color: '#B85C00', bgColor: '#FFF4E6' },
  beauty: { color: '#C41D7F', bgColor: '#FFF0F6' },
  digital: { color: '#1144BA', bgColor: '#EFF3FF' },
  food: { color: '#335519', bgColor: '#EDF7E6' },
}

export default function Index() {
  const navigate = useNavigate()
  const [searchKeyword, setSearchKeyword] = useState('')

  const cardList = useMemo(
    () =>
      INDUSTRY_CONFIGS.map((industry) => ({
        id: industry.id,
        title: `${industry.name}`,
        icon: IconSearch,
        desc: industry.description,
        color: INDUSTRY_COLORS[industry.id]?.color || '#333',
        bgColor: INDUSTRY_COLORS[industry.id]?.bgColor || '#f5f5f5',
      })),
    [],
  )

  // 根据搜索关键词过滤卡片
  const filteredCardList = useMemo(() => {
    if (!searchKeyword.trim()) return cardList
    const keyword = searchKeyword.toLowerCase()
    return cardList.filter(
      (item) =>
        item.title.toLowerCase().includes(keyword) ||
        item.desc.toLowerCase().includes(keyword)
    )
  }, [cardList, searchKeyword])

  // 点击卡片，切换行业并跳转到聊天页
  const handleCardClick = (industryId: string, title: string) => {
    console.log('[Index] 点击行业卡片:', industryId, title)
    setCurrentIndustry(industryId)
    navigate(`/chat?title=${encodeURIComponent(title)}`)
  }

  return (
    <div className={styles['index-page']}>
      <div className={styles.header}>
        <img className={styles.bg} src={IconBg} />
        <div className={styles.title}>AI 电商运营分析平台</div>
        <div className={styles.desc}>
          基于大模型的电商运营智能分析，覆盖销售、商品、竞品、达人等多维度
        </div>
      </div>

      <div className={styles['search-bar']}>
        <div className={styles['switch']}>
          <div onClick={() => message.info('暂未开放')} style={{ cursor: 'pointer' }}>我的</div>
          <div className={styles.active}>市场</div>
        </div>

        <div className={styles['search-bar__input']}>
          <Input
            prefix={<img src={IconSearch} />}
            placeholder="搜索应用"
            size="large"
            value={searchKeyword}
            onChange={(e) => setSearchKeyword(e.target.value)}
            allowClear
          />
        </div>
      </div>

      <div className={styles['card-list']}>
        {filteredCardList.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#999', width: '100%' }}>
            未找到匹配的应用
          </div>
        ) : filteredCardList.map((item) => (
          <div
            className={styles['card-item']}
            key={item.id}
            style={{
              backgroundColor: item.bgColor,
              color: item.color,
              cursor: 'pointer',
            }}
            onClick={() => handleCardClick(item.id, item.title)}
          >
            <div
              className={styles['card-item__icon']}
              style={{
                borderColor: item.color,
              }}
            >
              <img src={item.icon} />
            </div>

            <div className={styles['card-item__title']}>{item.title}</div>
            <div className={styles['card-item__desc']}>{item.desc}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
