import { type NextRequest, NextResponse } from "next/server"

// Mock API endpoint - in production, integrate with real financial data APIs
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const symbol = searchParams.get("symbol")

  if (!symbol) {
    return NextResponse.json({ error: "Symbol is required" }, { status: 400 })
  }

  // Mock response - replace with actual API calls to yfinance, Alpha Vantage, etc.
  const mockData = {
    symbol: symbol.toUpperCase(),
    name: `${symbol.toUpperCase()} Inc.`,
    price: Math.random() * 200 + 100,
    change: (Math.random() - 0.5) * 10,
    changePercent: (Math.random() - 0.5) * 5,
    volume: `${Math.floor(Math.random() * 100)}M`,
    marketCap: `${Math.floor(Math.random() * 5)}T`,
    pe: Math.random() * 50 + 10,
    signals: {
      overall: Math.random() > 0.5 ? "BUY" : Math.random() > 0.5 ? "SELL" : "HOLD",
      confidence: Math.floor(Math.random() * 30) + 70,
      technical: Math.random() > 0.5 ? "BUY" : "HOLD",
      fundamental: Math.random() > 0.5 ? "BUY" : "HOLD",
      ml_prediction: Math.random() > 0.5 ? "BUY" : "HOLD",
    },
  }

  return NextResponse.json(mockData)
}
