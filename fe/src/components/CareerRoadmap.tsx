import React from 'react';
import { Button } from "@/components/ui/button";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router";
import CareerRoadmapView from "@/components/CareerRoadmapView";
import { useInputForm } from "@/InputFormStore";

const CareerRoadmap = () => {
  const navigate = useNavigate();
  const [state] = useInputForm();
  
  
  const roadmapTrees = (state as any).api2Result?.tree ?? [];
  // 이미지의 실제 데이터 구조에 맞는 샘플 데이터

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-green-600/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-purple-600/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      {/* Header */}
      <header className="relative z-10 p-6">
        <nav className="flex justify-between items-center max-w-7xl mx-auto">
          <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            NextDev
          </div>
          <div className="flex gap-3">
            <Button 
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              onClick={() => navigate("/")}
            >
              완료
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="relative z-10 px-6 pt-8 pb-12">
        {roadmapTrees.length > 0 ? (
          <CareerRoadmapView trees={roadmapTrees} />
        ) : (
          <p className="text-center text-gray-400">로드맵 데이터를 불러오는 중입니다…</p>
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-gray-800 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-gray-400">
          <p>&copy; 2025 NextDev. 모든 권리 보유.</p>
        </div>
      </footer>
    </div>
  );
};

export default CareerRoadmap;