import { Badge } from "@/components/ui/badge"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"

interface Signal {
  symbol: string
  signal: "BUY" | "SELL" | "HOLD"
  confidence: number
  price: number
  target: number
  reason: string
}

interface SignalCardProps {
  signal: Signal
}

export function SignalCard({ signal }: SignalCardProps) {
  const getSignalColor = (signalType: string) => {
    switch (signalType) {
      case "BUY":
        return "bg-green-600 hover:bg-green-700"
      case "SELL":
        return "bg-red-600 hover:bg-red-700"
      default:
        return "bg-slate-600 hover:bg-slate-700"
    }
  }

  const getSignalIcon = (signalType: string) => {
    switch (signalType) {
      case "BUY":
        return <TrendingUp className="h-3 w-3" />
      case "SELL":
        return <TrendingDown className="h-3 w-3" />
      default:
        return <Minus className="h-3 w-3" />
    }
  }

  return (
    <div className="border rounded-lg p-3 hover:bg-slate-50 transition-colors">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <span className="font-semibold">{signal.symbol}</span>
          <Badge className={getSignalColor(signal.signal)}>
            {getSignalIcon(signal.signal)}
            <span className="ml-1">{signal.signal}</span>
          </Badge>
        </div>
        <span className="text-sm text-slate-600">{signal.confidence}%</span>
      </div>

      <div className="flex items-center justify-between text-sm mb-2">
        <span>Current: ${signal.price}</span>
        <span>Target: ${signal.target}</span>
      </div>

      <p className="text-xs text-slate-600">{signal.reason}</p>
    </div>
  )
}
