import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, PieChart } from "lucide-react"

export function PortfolioOverview() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <PieChart className="h-5 w-5" />
          <span>Portfolio</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">Total Value</span>
          <span className="font-semibold text-lg">$125,430</span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">Today's P&L</span>
          <span className="font-semibold text-green-600 flex items-center">
            <TrendingUp className="h-4 w-4 mr-1" />
            +$2,340 (1.9%)
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">Total Return</span>
          <span className="font-semibold text-green-600">+$18,430 (17.2%)</span>
        </div>

        <div className="space-y-2">
          <div className="text-sm font-medium">Top Holdings</div>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span>AAPL</span>
              <span>32%</span>
            </div>
            <div className="flex justify-between">
              <span>MSFT</span>
              <span>28%</span>
            </div>
            <div className="flex justify-between">
              <span>GOOGL</span>
              <span>22%</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
