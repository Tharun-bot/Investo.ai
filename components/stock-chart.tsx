"use client"

import { Line, LineChart, XAxis, YAxis, ResponsiveContainer, ReferenceLine } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const chartData = [
  { time: "09:30", price: 182.5, volume: 1200000 },
  { time: "10:00", price: 183.2, volume: 980000 },
  { time: "10:30", price: 184.1, volume: 1100000 },
  { time: "11:00", price: 183.8, volume: 850000 },
  { time: "11:30", price: 184.5, volume: 920000 },
  { time: "12:00", price: 185.2, volume: 750000 },
  { time: "12:30", price: 185.9, volume: 680000 },
  { time: "13:00", price: 186.1, volume: 720000 },
  { time: "13:30", price: 185.7, volume: 890000 },
  { time: "14:00", price: 186.3, volume: 1050000 },
  { time: "14:30", price: 185.92, volume: 980000 },
]

const chartConfig = {
  price: {
    label: "Price",
    color: "hsl(var(--chart-1))",
  },
}

interface StockChartProps {
  symbol: string
}

export function StockChart({ symbol }: StockChartProps) {
  return (
    <div className="space-y-4">
      <div className="h-[300px]">
        <ChartContainer config={chartConfig}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 12 }} />
              <YAxis
                domain={["dataMin - 1", "dataMax + 1"]}
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12 }}
              />
              <ChartTooltip content={<ChartTooltipContent />} />
              <ReferenceLine y={185} stroke="#ef4444" strokeDasharray="5 5" label="Resistance" />
              <ReferenceLine y={182.5} stroke="#22c55e" strokeDasharray="5 5" label="Support" />
              <Line type="monotone" dataKey="price" stroke="var(--color-price)" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      <div className="grid grid-cols-4 gap-4 text-sm">
        <div className="text-center">
          <div className="text-slate-600">Open</div>
          <div className="font-semibold">$182.50</div>
        </div>
        <div className="text-center">
          <div className="text-slate-600">High</div>
          <div className="font-semibold">$186.30</div>
        </div>
        <div className="text-center">
          <div className="text-slate-600">Low</div>
          <div className="font-semibold">$182.10</div>
        </div>
        <div className="text-center">
          <div className="text-slate-600">Close</div>
          <div className="font-semibold">$185.92</div>
        </div>
      </div>
    </div>
  )
}
