import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { X, ArrowRight } from "lucide-react";

interface ReusableSkillSelectProps {
  title: string | React.ReactNode;
  description: string;
  availableSkills: string[];
  onSubmit: (skills: string[]) => void;
}

const ReusableSkillSelect = ({
  title,
  description,
  availableSkills,
  onSubmit,
}: ReusableSkillSelectProps) => {
  const [skills, setSkills] = useState<string[]>([]);

  const toggleSkill = (skill: string) => {
    setSkills((prev) =>
      prev.includes(skill)
        ? prev.filter((s) => s !== skill)
        : [...prev, skill]
    );
  };

  const removeSkill = (skillToRemove: string) => {
    setSkills(skills.filter((s) => s !== skillToRemove));
  };

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-600/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-cyan-600/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      {/* Header */}
      <header className="relative z-10 p-6">
        <nav className="flex justify-between items-center max-w-7xl mx-auto">
          <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            NextDev
          </div>
        </nav>
      </header>

      {/* Main */}
      <main className="relative z-10 max-w-4xl mx-auto px-6 pt-12 pb-12">
        <div className="space-y-8 animate-fade-in">
          {/* Title */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-white via-blue-200 to-purple-200 bg-clip-text text-transparent">
              {title}
            </h1>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">{description}</p>
          </div>

          {/* Skill Grid */}
          <div className="bg-gray-900/50 border border-gray-800 backdrop-blur-sm rounded-2xl p-8 space-y-6">
            <p className="text-sm text-gray-400 text-center">
              다룰 수 있는 기술을 클릭해서 선택하세요. <br />
              없으시면 그냥 넘기셔도 됩니다.
            </p>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {availableSkills.map((skill) => {
                const isSelected = skills.includes(skill);
                return (
                  <button
                    key={skill}
                    onClick={() => toggleSkill(skill)}
                    className={`px-4 py-2 rounded-full border transition-all text-sm font-medium ${
                      isSelected
                        ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white border-blue-500 shadow-md"
                        : "bg-gray-800/50 text-gray-300 border-gray-700 hover:bg-gray-700"
                    }`}
                  >
                    {skill}
                  </button>
                );
              })}
            </div>

            {/* 선택된 목록 */}
            {skills.length > 0 && (
              <div className="space-y-4 animate-fade-in">
                <h3 className="text-lg font-semibold text-white">선택된 항목 ({skills.length}개)</h3>
                <div className="flex flex-wrap gap-3">
                  {skills.map((skill) => (
                    <div
                      key={skill}
                      className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-full px-4 py-2 flex items-center gap-2"
                    >
                      <span className="text-white font-medium">{skill}</span>
                      <button
                        onClick={() => removeSkill(skill)}
                        className="text-gray-400 hover:text-white transition-colors"
                      >
                        <X className="cursor-pointer h-4 w-4" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Submit */}
          <div className="flex justify-center pt-8">
            <Button
              onClick={() => onSubmit(skills)}
              className="cursor-pointer bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
            >
              다음 단계로
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ReusableSkillSelect;
