import { Button } from "@/components/ui/button";
import { CheckCircle, Loader2, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router";
import { useEffect, useState } from "react";

const AnalysisProgress = () => {
    const navigate = useNavigate();
    const [isFirstStageComplete, setIsFirstStageComplete] = useState(false);
    const [showSecondStage, setShowSecondStage] = useState(false);

    useEffect(() => {
        // Simulate first stage completion
        const timer1 = setTimeout(() => {
            setIsFirstStageComplete(true);
        }, 1500);

        // Show second stage message
        const timer2 = setTimeout(() => {
            setShowSecondStage(true);
        }, 3000);

        return () => {
            clearTimeout(timer1);
            clearTimeout(timer2);
        };
    }, []);

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
                    <div 
                        className="cursor-pointer text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
                        onClick={()=>navigate("/")}
                    >
                        NextDev
                    </div>
                </nav>
            </header>

            {/* Main Content */}
            <main className="relative z-10 max-w-4xl mx-auto px-6 pt-20 pb-12">
                <div className="text-center space-y-12">
                    {/* Progress Section */}
                    <div className="space-y-8">
                        {/* Step 1 */}
                        <div className={`transition-all duration-1000 ${isFirstStageComplete ? 'animate-scale-in' : ''}`}>
                            <div className="flex items-center justify-center space-x-4 mb-6">
                                {isFirstStageComplete ? (
                                    <CheckCircle className="h-16 w-16 text-green-400 animate-scale-in" />
                                ) : (
                                    <Loader2 className="h-16 w-16 text-blue-400 animate-spin" />
                                )}
                                <div className="text-left">
                                    <h2 className="text-3xl font-bold text-white">1단계 분석</h2>
                                    <p className="text-gray-400">기술 스택 검토</p>
                                </div>
                            </div>

                            {isFirstStageComplete && (
                                <div className="bg-green-900/20 border border-green-500/30 rounded-2xl p-8 animate-fade-in">
                                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent mb-4">
                                        1단계 분석이 끝났습니다.
                                    </h1>
                                    <p className="text-xl text-gray-300">
                                        입력하신 기술 스택이 성공적으로 분석되었습니다.
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* Step 2 */}
                        {showSecondStage && (
                            <div className="animate-fade-in" style={{ animationDelay: '0.5s' }}>
                                <div className="flex items-center justify-center space-x-4 mb-6">
                                    <Loader2 className="h-16 w-16 text-purple-400 animate-spin" />
                                    <div className="text-left">
                                        <h2 className="text-3xl font-bold text-white">2단계 분석</h2>
                                        <p className="text-gray-400">이력 데이터 취합</p>
                                    </div>
                                </div>

                                <div className="bg-purple-900/20 border border-purple-500/30 rounded-2xl p-8">
                                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
                                        <span className="block my-2">이제 2단계 분석을 위해</span>
                                        <span className="block">이력을 취합합니다.</span>
                                    </h1>
                                    <p className="text-xl text-gray-300">
                                        계속 진행해주세요.
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Progress Bar */}
                    <div className="w-full max-w-2xl mx-auto">
                        <div className="bg-gray-800 rounded-full h-3 overflow-hidden">
                            <div
                                className={`h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-2000 ease-out ${isFirstStageComplete ? 'w-1/2' : 'w-1/4'
                                    } ${showSecondStage ? 'w-3/4' : ''}`}
                            />
                        </div>
                        <div className="flex justify-between mt-3 text-sm text-gray-400">
                            <span>시작</span>
                            <span>분석 중</span>
                            <span>완료</span>
                        </div>
                    </div>

                    {/* Navigation */}
                    {showSecondStage && (
                        <div className="flex justify-center pt-8 animate-fade-in" style={{ animationDelay: '1s' }}>
                            <Button
                                className="cursor-pointer bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-4 text-lg font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
                                onClick = {()=>{navigate("/cert")}}
                            >
                                다음 단계로
                                <ArrowRight className="ml-2 h-5 w-5" />
                            </Button>
                        </div>
                    )}
                </div>
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

export default AnalysisProgress;