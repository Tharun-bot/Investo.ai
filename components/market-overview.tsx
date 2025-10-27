import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, TrendingUp, TrendingDown } from "lucide-react"

export function MarketOverview() {
  const marketData = [
    { name: "S&P 500", value: "4,567.89", change: "+0.8%", positive: true },
    { name: "NASDAQ", value: "14,234.56", change: "+1.2%", positive: true },
    { name: "DOW", value: "34,567.12", change: "-0.3%", positive: false },
    { name: "VIX", value: "18.45", change: "-2.1%", positive: false },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <BarChart3 className="h-5 w-5" />
          <span>Market Overview</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {marketData.map((item, index) => (
          <div key={index} className="flex items-center justify-between">
            <div>
              <div className="font-medium text-sm">{item.name}</div>
              <div className="text-xs text-slate-600">{item.value}</div>
            </div>
            <div className={`flex items-center text-sm ${item.positive ? "text-green-600" : "text-red-600"}`}>
              {item.positive ? <TrendingUp className="h-3 w-3 mr-1" /> : <TrendingDown className="h-3 w-3 mr-1" />}
              {item.change}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
