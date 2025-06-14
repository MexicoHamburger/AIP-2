import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { X, ArrowRight, CalendarIcon, Plus } from "lucide-react";
import { useNavigate } from "react-router";
import { format } from "date-fns";
import { cn } from "@/lib/utils";
import YearMonthSelect from "./YearMonthSelect";
import { useInputForm } from "@/InputFormStore";

interface CareerExperience {
  id: string;
  role: string;
  career: string;
  startDate: Date;
  endDate?: Date;
  description: string;
}

const CAREER_TYPES = [
  "개인 프로젝트", "인턴십", "주니어 개발자로 근무 (중견기업 이상)", "동아리 활동", "연구소 / 랩실",
  "해커톤", "공모전", "유지보수 작업", "스타트업 근무",
] as const;

const ROLE_TYPES = [
  "프론트엔드 개발", "백엔드 개발", "인공지능 개발", "UX/UI 개발", "게임 개발",
  "유지보수", "앱 개발", "데이터 엔지니어링", "풀스택 개발",
] as const;


const CAREER_MAP: Record<string, string> = {
  "개인 프로젝트": "TYPE_Proj",
  "인턴십": "TYPE_Intern",
  "주니어 개발자로 근무 (중견기업 이상)": "TYPE_Junior",
  "동아리 활동": "TYPE_Club",
  "연구소 / 랩실 ": "TYPE_Research",
  "해커톤": "TYPE_Hackathon",
  "공모전": "TYPE_Contest",
  "유지보수 작업": "TYPE_Maintenance",
  "스타트업 근무": "TYPE_Startup"
};

const ROLE_MAP: Record<string, string> = {
  "프론트엔드 개발": "ROLE_FE",
  "백엔드 개발": "ROLE_BE",
  "인공지능 개발": "ROLE_AI",
  "UX/UI 개발": "ROLE_UXUI",
  "게임 개발": "ROLE_GAME",
  "유지보수": "ROLE_DEVOPS",
  "앱 개발": "ROLE_APP",
  "데이터 엔지니어링": "ROLE_DE",
  "풀스택 개발": "ROLE_FULLSTACK"
};

const encodeExperiences = (exps: CareerExperience[]) =>
  exps.map((e) => `${CAREER_MAP[e.career]}|${ROLE_MAP[e.role]}`);

const sortByStartAsc = (a: CareerExperience, b: CareerExperience) =>
  a.startDate.getTime() - b.startDate.getTime();

const CareerInput = () => {
  const [experiences, setExperiences] = useState<CareerExperience[]>([]);
  const [currentExperience, setCurrentExperience] = useState({
    role: "",
    career: "",
    startDate: undefined as Date | undefined,
    endDate: undefined as Date | undefined,
    description: "",
  });
  const navigate = useNavigate();
  const [state, dispatch] = useInputForm();

  const addExperience = () => {
    if (currentExperience.role && currentExperience.career && currentExperience.startDate) {
      const newExperience: CareerExperience = {
        id: Date.now().toString(),
        role: currentExperience.role,
        career: currentExperience.career,
        startDate: currentExperience.startDate,
        endDate: currentExperience.endDate,
        description: currentExperience.description,
      };

      setExperiences(prev => [...prev, newExperience].sort(sortByStartAsc));

      // Reset form
      setCurrentExperience({
        role: "",
        career: "",
        startDate: undefined,
        endDate: undefined,
        description: "",
      });
    }
  };

  const removeExperience = (id: string) => {
    setExperiences(prev => prev.filter(exp => exp.id !== id).sort(sortByStartAsc));
  };

  const isFormValid =
    !!currentExperience.role &&
    !!currentExperience.career &&
    !!currentExperience.startDate;

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-600/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-cyan-600/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      {/* Header */}
      <header className="relative z-10 p-6">
        <nav className="flex justify-between items-center max-w-7xl mx-auto">
          <div
            className="cursor-pointer text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
            onClick={() => navigate("/")}
          >
            NextDev
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-4xl mx-auto px-6 pt-12 pb-12">
        <div className="space-y-8 animate-fade-in">
          {/* Title */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-white via-blue-200 to-purple-200 bg-clip-text text-transparent">
              경력 정보 입력
            </h1>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              개발 관련 경력 사항을 입력해주세요
            </p>
          </div>

          {/* Input Form */}
          <div className="bg-gray-900/50 border border-gray-800 backdrop-blur-sm rounded-2xl p-8 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* 역할(ROLE) */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  역할(Role)
                </label>
                <Select
                  value={currentExperience.role}
                  onValueChange={(value) =>
                    setCurrentExperience((prev) => ({ ...prev, role: value }))
                  }
                >
                  <SelectTrigger className="w-full bg-gray-800/50 border-gray-700 text-white focus:border-blue-500 h-12">
                    <SelectValue placeholder="선택하세요" />
                  </SelectTrigger>
                  <SelectContent className="bg-gray-800 border-gray-700 text-white">
                    {ROLE_TYPES.map((type) => (
                      <SelectItem
                        key={type}
                        value={type}
                        className="focus:bg-gray-700 focus:text-white hover:bg-gray-700"
                      >
                        {type}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* 유형(COMPANY) */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  활동 유형(Type)
                </label>
                <Select
                  value={currentExperience.career}
                  onValueChange={(value) =>
                    setCurrentExperience((prev) => ({ ...prev, career: value }))
                  }
                >
                  <SelectTrigger className="w-full bg-gray-800/50 border-gray-700 text-white focus:border-blue-500 h-12">
                    <SelectValue placeholder="선택하세요" />
                  </SelectTrigger>
                  <SelectContent className="bg-gray-800 border-gray-700 text-white">
                    {CAREER_TYPES.map((type) => (
                      <SelectItem
                        key={type}
                        value={type}
                        className="focus:bg-gray-700 focus:text-white hover:bg-gray-700"
                      >
                        {type}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">시작일</label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className={cn(
                        "w-full justify-start text-left font-normal bg-gray-800/50 border-gray-700 text-white hover:bg-gray-700",
                        !currentExperience.startDate && "text-gray-400"
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {currentExperience.startDate ? format(currentExperience.startDate, "yyyy년 MM월") : "시작일 선택"}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <YearMonthSelect
                      value={currentExperience.startDate}
                      onChange={(date) =>
                        setCurrentExperience((prev) => ({ ...prev, startDate: date }))
                      }
                    />
                  </PopoverContent>
                </Popover>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">종료일</label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className={cn(
                        "w-full justify-start text-left font-normal bg-gray-800/50 border-gray-700 text-white hover:bg-gray-700",
                        !currentExperience.endDate && "text-gray-400"
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {currentExperience.endDate ? format(currentExperience.endDate, "yyyy년 MM월") : "종료일 선택 (선택사항)"}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <YearMonthSelect
                      value={currentExperience.endDate}
                      onChange={(date) =>
                        setCurrentExperience((prev) => ({ ...prev, endDate: date }))
                      }
                    />
                  </PopoverContent>
                </Popover>
              </div>
            </div>

            <div className="flex justify-center">
              <Button
                onClick={addExperience}
                disabled={!isFormValid}
                className="bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Plus className="mr-2 h-4 w-4" />
                경력 추가
              </Button>
            </div>
          </div>

          {/* Experience Preview */}
          {experiences.length > 0 && (
            <div className="bg-gray-900/50 border border-gray-800 backdrop-blur-sm rounded-2xl p-8 space-y-6 animate-fade-in">
              <h3 className="text-2xl font-semibold text-white text-center">입력된 경력 ({experiences.length}개)</h3>
              <div className="space-y-4">
                {experiences.map((exp) => (
                  <div
                    key={exp.id}
                    className="bg-gradient-to-r from-blue-600/10 to-purple-600/10 border border-blue-500/20 rounded-xl p-6 flex justify-between items-start"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h4 className="text-lg font-semibold text-white">{exp.role}</h4>
                        <span className="text-blue-300">@{exp.career}</span>
                      </div>
                      <div className="text-gray-300 text-sm mb-2">
                        {format(exp.startDate, "yyyy년 MM월")} - {exp.endDate ? format(exp.endDate, "yyyy년 MM월") : "현재"}
                      </div>
                      {exp.description && (
                        <p className="text-gray-400 text-sm">{exp.description}</p>
                      )}
                    </div>
                    <button
                      onClick={() => removeExperience(exp.id)}
                      className="text-gray-400 hover:text-white transition-colors ml-4"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Navigation */}
          <div className="flex justify-center pt-8">
            <Button
              className="cursor-pointer bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
              onClick={() => {
                const encoded = encodeExperiences(experiences);
                dispatch({ type: "SET_CAREER", payload: encoded });
                navigate("/analyzing");
              }}
            >
              다음 단계로
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
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

export default CareerInput;