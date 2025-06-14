import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ExternalLink, Loader2 } from "lucide-react";

interface PracticeItem {
  category: string;
  name: string;
  reason: string;
  fields: string[];
  skills: string[];
  description: string;
  link: string;
}

interface CareerDetailData {
  title: string;
  practice_items: {
    step1: PracticeItem;
    step2: PracticeItem;
  };
  total_reason: string;
}

interface CareerDetailPopupProps {
  isOpen: boolean;
  onClose: () => void;
  isLoading: boolean;
  data: CareerDetailData | null;
}

const CareerDetailPopup: React.FC<CareerDetailPopupProps> = ({
  isOpen,
  onClose,
  isLoading,
  data
}) => {
  const renderPracticeItem = (step: string, item: PracticeItem) => (
    <Card key={step} className="bg-gray-800/50 border-gray-700">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg text-white flex items-center gap-2">
            {item.name}
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-gray-300 text-sm leading-relaxed">{item.description}</p>
        
        <div>
          <h4 className="text-white font-medium mb-2">선택 이유</h4>
          <p className="text-gray-400 text-sm leading-relaxed">{item.reason}</p>
        </div>

        <div>
          <h4 className="text-white font-medium mb-2">주요 분야</h4>
          <div className="flex flex-wrap gap-2">
            {item.fields.map((field, index) => (
              <Badge key={index} className="bg-blue-500/20 text-blue-300 border-blue-500/30 text-xs">
                {field}
              </Badge>
            ))}
          </div>
        </div>

        <div>
          <h4 className="text-white font-medium mb-2">핵심 기술</h4>
          <div className="flex flex-wrap gap-2">
            {item.skills.map((skill, index) => (
              <Badge key={index} className="bg-green-500/20 text-green-300 border-green-500/30 text-xs">
                {skill}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="w-full max-w-[90vw] sm:max-w-7xl md:max-w-7xl lg:max-w-7xl xl:max-w-7xl max-h-[80vh] overflow-y-auto bg-gray-900 border-gray-700 text-white">
        <DialogHeader>
          <DialogTitle className="text-xl bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
            {isLoading ? "진로 정보 분석 중..." : data?.title || "진로 세부 정보"}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="flex flex-col items-center gap-4">
                <Loader2 className="h-8 w-8 animate-spin text-blue-400" />
                <p className="text-gray-400">로딩 중...</p>
              </div>
            </div>
          ) : data ? (
            <>
              <div className="grid md:grid-cols-2 gap-6">
                {renderPracticeItem("step1", data.practice_items.step1)}
                {renderPracticeItem("step2", data.practice_items.step2)}
              </div>
              
              <Card className="bg-gray-800/30 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white">전체 추천 이유</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300 leading-relaxed">{data.total_reason}</p>
                </CardContent>
              </Card>
            </>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-400">데이터를 불러올 수 없습니다.</p>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default CareerDetailPopup;