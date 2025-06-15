import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { DollarSign, TrendingUp, MapPin, Briefcase, Star } from "lucide-react";

interface SalaryData {
  보완후연봉: string;
  예상연봉_현재: string;
  추천스택: string;
  추천직무: string;
  예상만족도: number;
}

interface SalaryResultViewProps {
  results: SalaryData[];
  title?: string;
}

const SalaryResultView: React.FC<SalaryResultViewProps> = ({
  results,
  title = "급여 분석 결과"
}) => {
  const formatSalary = (salary: string) => {
    // "95,364,384 / 88,660,064 / 89,140,488 원" 형식을 파싱
    const numbers = salary.match(/[\d,]+/g);
    if (numbers && numbers.length >= 3) {
      return {
        max: numbers[0],
        avg: numbers[1],
        min: numbers[2]
      };
    }
    return { max: salary, avg: salary, min: salary };
  };

  const getStackColor = (stack: string) => {
    const colors = {
      'Rust': 'bg-orange-500/20 text-orange-300 border-orange-500/30',
      'Swift': 'bg-blue-500/20 text-blue-300 border-blue-500/30',
      'Go': 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
      'Developer': 'bg-purple-500/20 text-purple-300 border-purple-500/30',
      'full-stack': 'bg-green-500/20 text-green-300 border-green-500/30',
      'embedded': 'bg-red-500/20 text-red-300 border-red-500/30',
      'back-end': 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30'
    };

    for (const [key, value] of Object.entries(colors)) {
      if (stack.toLowerCase().includes(key.toLowerCase())) {
        return value;
      }
    }
    return 'bg-gray-500/20 text-gray-300 border-gray-500/30';
  };

  const renderStars = (score: number) => {
    const fullStars = Math.floor(score / 2); // 10점을 5점으로 변환
    const hasHalfStar = (score % 2) >= 1;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    return (
      <div className="flex items-center gap-1">
        {/* 꽉 찬 별 */}
        {Array.from({ length: fullStars }).map((_, i) => (
          <Star key={`full-${i}`} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
        ))}

        {/* 반 별 */}
        {hasHalfStar && (
          <div className="relative">
            <Star className="h-4 w-4 text-gray-600" />
            <div className="absolute inset-0 overflow-hidden" style={{ width: '50%' }}>
              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
            </div>
          </div>
        )}

        {/* 빈 별 */}
        {Array.from({ length: emptyStars }).map((_, i) => (
          <Star key={`empty-${i}`} className="h-4 w-4 text-gray-600" />
        ))}

        <span className="text-xs text-gray-400 ml-1">({score}/10)</span>
      </div>
    );
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-6 space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
          {title}
        </h2>
        <p className="text-gray-400">총 {results.length}개의 분석 결과</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {results.map((result, index) => {
          const salaryData = formatSalary(result.보완후연봉);
          const stackArr = result.추천스택.split(",").map(s => s.trim());
          const currentSalary = result.예상연봉_현재?.replace(/[^\d,]/g, '') || 'N/A';

          return (
            <Card key={index} className="bg-gray-900/50 border-gray-800/50 backdrop-blur-sm hover:bg-gray-900/70 transition-all duration-300 hover:scale-105">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-semibold text-white flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-green-400" />
                    결과 #{index + 1}
                  </CardTitle>
                  <Badge variant="outline" className="bg-blue-500/10 text-blue-300 border-blue-500/30">
                    분석완료
                  </Badge>
                </div>
              </CardHeader>

              <CardContent className="space-y-6">
                {/* 급여 정보 */}
                <div className="space-y-4">
                  <div className="flex items-center gap-2 text-sm font-medium text-gray-300">
                    <TrendingUp className="h-4 w-4" />
                    급여 범위
                  </div>

                  <div className="bg-gradient-to-r from-green-600/10 to-emerald-600/10 border border-green-500/20 rounded-lg p-4">
                    <div className="grid grid-cols-3 gap-3 text-center">
                      {/* 최고 구간 */}
                      <div>
                        <div className="text-xs mb-1 font-semibold text-green-300">
                          {stackArr[0] || "-"}
                        </div>
                        <div className="text-sm font-bold text-green-300">
                          {salaryData.max}
                        </div>
                      </div>

                      {/* 평균 구간 */}
                      <div>
                        <div className="text-xs mb-1 font-semibold text-blue-300">
                          {stackArr[1] || "-"}
                        </div>
                        <div className="text-sm font-bold text-blue-300">
                          {salaryData.avg}
                        </div>
                      </div>

                      {/* 최소 구간 */}
                      <div>
                        <div className="text-xs mb-1 font-semibold text-orange-300">
                          {stackArr[2] || "-"}
                        </div>
                        <div className="text-sm font-bold text-orange-300">
                          {salaryData.min}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* 현재 예상 연봉 */}
                  <div className="bg-gray-800/40 border border-gray-700/30 rounded-lg p-3">
                    <div className="text-xs text-gray-400 mb-1">현재 예상 연봉</div>
                    <div className="text-lg font-bold text-white">
                      {currentSalary} 원
                    </div>
                  </div>
                </div>

                <Separator className="bg-gray-700/30" />

                {/* 직무 정보 */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm font-medium text-gray-300">
                    <Briefcase className="h-4 w-4" />
                    직무 정보
                  </div>

                  <div className="space-y-3">
                    <div>
                      <div className="text-xs text-gray-400 mb-2">추천 스택</div>
                      <div className="flex flex-wrap gap-1">
                        {result.추천스택.split(',').map((stack, idx) => (
                          <Badge key={idx} className={`${getStackColor(stack.trim())} text-xs`}>
                            {stack.trim()}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div>
                      <div className="text-xs text-gray-400 mb-2">추천 직무</div>
                      <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30 text-xs">
                        {result.추천직무}
                      </Badge>
                    </div>
                    <div>
                      <div className="text-xs text-gray-400 mb-2">직무 만족도</div>
                      <div className="bg-yellow-500/5 border border-yellow-500/20 rounded-lg p-3">
                        {renderStars(result.예상만족도)}
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default SalaryResultView;