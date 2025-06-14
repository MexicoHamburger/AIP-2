import React from 'react';
import { Button } from "@/components/ui/button";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router";
import SalaryResultView from "@/components/SalaryResultView";
import { useInputForm } from "@/InputFormStore";

const SalaryAnalysis = () => {
    const navigate = useNavigate();
    const [state] = useInputForm();          // ← 1차 API 결과 읽기

    // 샘플 데이터 (실제로는 API에서 받아올 데이터)
    const rawResults = (state as any).api1Result?.results ?? [];

    /* ② 필요한 키만 뽑아 프론트에서 쓰기 좋은 형태로 변환 */
    const results = rawResults.map((r: any) => ({
        보완후연봉: r["보완 후 연봉"] ?? "",
        예상연봉_현재: r["예상 연봉(현재)"] ?? "",
        추천스택: r["추천 스택"] ?? "",
        추천직무: r["추천 직무"] ?? ""
    }));


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
                    <Button
                        className="cursor-pointer bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                        onClick={() => navigate("/results-2")}
                    >
                        다음으로
                        <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </nav>
            </header>

            {/* Main Content */}
            <main className="relative z-10 px-6 pt-8 pb-12">
                <SalaryResultView results={results} />
            </main>

            {/* Footer */}
            <footer className="relative z-10 border-t border-gray-800 mt-20">
                <div className="max-w-7xl mx-auto px-6 py-8 text-center text-gray-400">
                    <p>&copy; 2025 NextDev. All Rights Reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default SalaryAnalysis;