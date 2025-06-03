import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowRight, Sparkles, Target, TrendingUp, Users } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-600/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse"/>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-cyan-600/5 rounded-full blur-3xl animate-pulse"/>
      </div>

      {/* Header */}
      <header className="relative z-10 p-6">
        <nav className="flex justify-between items-center max-w-7xl mx-auto">
          <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            NextDev
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 pt-20 pb-12">
        <div className="text-center space-y-8">
          {/* Main Title */}
          <div className="space-y-4 animate-fade-in">
            <h1 className="text-6xl md:text-8xl font-bold bg-gradient-to-r from-white via-blue-200 to-purple-200 bg-clip-text text-transparent leading-tight">
              NextDev
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              당신의 개발 이력을 분석하여<br />
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent font-semibold">
                맞춤형 진로 로드맵
              </span>을 제안해드립니다
            </p>
          </div>

          {/* CTA Button */}
          <div className="animate-fade-in">
            <Button 
              size="lg" 
              className="cursor-pointer bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
            >
              진로 로드맵 받아보기
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>

          {/* Feature Cards */}
          <div className="grid md:grid-cols-3 gap-6 mt-20 animate-fade-in">
            <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm hover:bg-gray-900/70 transition-all duration-300 hover:scale-105">
              <CardContent className="p-6 text-center space-y-4">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mx-auto">
                  <Target className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white">이력 분석</h3>
                <p className="text-gray-400">
                  개발 경험과 스킬을 AI가 정확히 분석하여 현재 수준을 파악합니다
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm hover:bg-gray-900/70 transition-all duration-300 hover:scale-105">
              <CardContent className="p-6 text-center space-y-4">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mx-auto">
                  <TrendingUp className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white">맞춤 로드맵</h3>
                <p className="text-gray-400">
                  목표와 현재 실력에 맞는 단계별 학습 계획을 제시합니다
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm hover:bg-gray-900/70 transition-all duration-300 hover:scale-105">
              <CardContent className="p-6 text-center space-y-4">
                <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-lg flex items-center justify-center mx-auto">
                  <Sparkles className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white">AI 추천</h3>
                <p className="text-gray-400">
                  최신 기술 트렌드와 시장 수요를 반영한 진로를 추천합니다
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Stats Section */}
          <div className="grid grid-cols-3 gap-8 mt-20 animate-fade-in">
            <div className="text-center">
              <div className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                5K+
              </div>
              <div className="text-gray-400 mt-2">분석된 이력서</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                95%
              </div>
              <div className="text-gray-400 mt-2">만족도</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
                500+
              </div>
              <div className="text-gray-400 mt-2">성공 사례</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-gray-800 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-gray-400">
          <p>&copy; 2025 NextDev. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;