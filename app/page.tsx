"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { TrendingUp, TrendingDown, Search, Activity, Brain, Target } from "lucide-react"
import { StockChart } from "@/components/stock-chart"
import { SignalCard } from "@/components/signal-card"
import { PortfolioOverview } from "@/components/portfolio-overview"
import { MarketOverview } from "@/components/market-overview"

// Mock data - in real app, this would come from your API
const mockStockData = {
  symbol: "AAPL",
  name: "Apple Inc.",
  price: 185.92,
  change: 2.34,
  changePercent: 1.28,
  volume: "52.3M",
  marketCap: "2.89T",
  pe: 28.5,
  signals: {
    overall: "BUY",
    confidence: 75,
    technical: "BUY",
    fundamental: "HOLD",
    ml_prediction: "BUY",
  },
}

const mockSignals = [
  {
    symbol: "AAPL",
    signal: "BUY",
    confidence: 85,
    price: 185.92,
    target: 195.0,
    reason: "Strong earnings momentum + technical breakout",
  },
  {
    symbol: "MSFT",
    signal: "HOLD",
    confidence: 72,
    price: 378.85,
    target: 385.0,
    reason: "Consolidation phase, await next catalyst",
  },
  {
    symbol: "GOOGL",
    signal: "BUY",
    confidence: 78,
    price: 138.21,
    target: 145.0,
    reason: "AI developments driving growth",
  },
  {
    symbol: "TSLA",
    signal: "SELL",
    confidence: 68,
    price: 248.5,
    target: 230.0,
    reason: "Overvalued metrics, profit-taking recommended",
  },
]

export default function InvestoAI() {
  const [searchSymbol, setSearchSymbol] = useState("")
  const [selectedStock, setSelectedStock] = useState(mockStockData)
  const [signals, setSignals] = useState(mockSignals)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // In real app, fetch stock data for searchSymbol
    console.log("Searching for:", searchSymbol)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <Brain className="h-8 w-8 text-blue-600" />
                <h1 className="text-2xl font-bold text-slate-900">Investo.ai</h1>
              </div>
              <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                AI-Powered
              </Badge>
            </div>

            <form onSubmit={handleSearch} className="flex items-center space-x-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                <Input
                  type="text"
                  placeholder="Search stocks (e.g., AAPL)"
                  value={searchSymbol}
                  onChange={(e) => setSearchSymbol(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              <Button type="submit">Search</Button>
            </form>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Stock Overview */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-2xl">{selectedStock.symbol}</CardTitle>
                    <CardDescription>{selectedStock.name}</CardDescription>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold">${selectedStock.price}</div>
                    <div
                      className={`flex items-center ${selectedStock.change >= 0 ? "text-green-600" : "text-red-600"}`}
                    >
                      {selectedStock.change >= 0 ? (
                        <TrendingUp className="h-4 w-4 mr-1" />
                      ) : (
                        <TrendingDown className="h-4 w-4 mr-1" />
                      )}
                      ${selectedStock.change} ({selectedStock.changePercent}%)
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div className="text-center">
                    <div className="text-sm text-slate-600">Volume</div>
                    <div className="font-semibold">{selectedStock.volume}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-slate-600">Market Cap</div>
                    <div className="font-semibold">${selectedStock.marketCap}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-slate-600">P/E Ratio</div>
                    <div className="font-semibold">{selectedStock.pe}</div>
                  </div>
                </div>

                {/* AI Signal */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <Target className="h-5 w-5 text-blue-600" />
                      <span className="font-semibold text-blue-900">AI Signal</span>
                    </div>
                    <Badge
                      variant={
                        selectedStock.signals.overall === "BUY"
                          ? "default"
                          : selectedStock.signals.overall === "SELL"
                            ? "destructive"
                            : "secondary"
                      }
                      className={selectedStock.signals.overall === "BUY" ? "bg-green-600" : ""}
                    >
                      {selectedStock.signals.overall}
                    </Badge>
                  </div>
                  <div className="flex items-center space-x-4 text-sm">
                    <div>
                      Confidence: <span className="font-semibold">{selectedStock.signals.confidence}%</span>
                    </div>
                    <div>
                      Technical: <span className="font-semibold">{selectedStock.signals.technical}</span>
                    </div>
                    <div>
                      Fundamental: <span className="font-semibold">{selectedStock.signals.fundamental}</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Price Chart & Technical Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                <StockChart symbol={selectedStock.symbol} />
              </CardContent>
            </Card>

            {/* Analysis Tabs */}
            <Card>
              <CardHeader>
                <CardTitle>Detailed Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="technical" className="w-full">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="technical">Technical</TabsTrigger>
                    <TabsTrigger value="fundamental">Fundamental</TabsTrigger>
                    <TabsTrigger value="ml">ML Insights</TabsTrigger>
                  </TabsList>

                  <TabsContent value="technical" className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <h4 className="font-semibold">Support & Resistance</h4>
                        <div className="text-sm space-y-1">
                          <div>Support: $182.50</div>
                          <div>Resistance: $188.00</div>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <h4 className="font-semibold">Indicators</h4>
                        <div className="text-sm space-y-1">
                          <div>RSI: 58.2 (Neutral)</div>
                          <div>MACD: Bullish crossover</div>
                        </div>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="fundamental" className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <h4 className="font-semibold">Valuation</h4>
                        <div className="text-sm space-y-1">
                          <div>P/E: 28.5 (Fair)</div>
                          <div>PEG: 1.2 (Reasonable)</div>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <h4 className="font-semibold">Growth</h4>
                        <div className="text-sm space-y-1">
                          <div>Revenue Growth: 8.2%</div>
                          <div>EPS Growth: 12.1%</div>
                        </div>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="ml" className="space-y-4">
                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="flex items-center space-x-2 mb-3">
                        <Brain className="h-5 w-5 text-purple-600" />
                        <h4 className="font-semibold">ML Model Prediction</h4>
                      </div>
                      <div className="space-y-2 text-sm">
                        <div>Model Accuracy: 75%</div>
                        <div>Prediction: BUY with 85% confidence</div>
                        <div>Key Factors: Earnings momentum, technical breakout pattern</div>
                        <div>Risk Level: Medium</div>
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Portfolio Overview */}
            <PortfolioOverview />

            {/* Market Overview */}
            <MarketOverview />

            {/* Recent Signals */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="h-5 w-5" />
                  <span>Recent Signals</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {signals.map((signal, index) => (
                  <SignalCard key={index} signal={signal} />
                ))}
              </CardContent>
            </Card>

            {/* Performance Stats */}
            <Card>
              <CardHeader>
                <CardTitle>AI Performance</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Overall Accuracy</span>
                  <span className="font-semibold">75%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Successful Signals</span>
                  <span className="font-semibold text-green-600">142/189</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Avg Return</span>
                  <span className="font-semibold text-green-600">+8.3%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Risk Score</span>
                  <span className="font-semibold text-yellow-600">Medium</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
