import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { X, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router";

interface SkillItem {
    name: string;
    desc: string|React.ReactNode;
}
interface CertSelectProps {
    title: string | React.ReactNode;
    description: string;
    availableSkills: SkillItem[];
    onSubmit: (skills: string[]) => void;
}

const CertSelect = ({
    title,
    description,
    availableSkills,
    onSubmit,
}: CertSelectProps) => {
    const [skills, setSkills] = useState<string[]>([]);
    const navigate = useNavigate();

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
                    <div
                        className="cursor-pointer text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
                        onClick={() => navigate("/")}>
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

                        <div className="flex flex-col divide-y divide-gray-800">
                            {availableSkills.map(({ name, desc }) => {
                                const selected = skills.includes(name);
                                return (
                                    <div
                                        key={name}
                                        className="flex items-center gap-4 py-3 first:pt-0 last:pb-0"
                                    >
                                        <button
                                            onClick={() => toggleSkill(name)}
                                            className={`w-40 flex-shrink-0 px-4 py-2 rounded-full border text-sm font-medium transition-all
      ${selected
                                                    ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white border-blue-500 shadow-md"
                                                    : "bg-gray-800/50 text-gray-300 border-gray-700 hover:bg-gray-700"}`}
                                        >
                                            {name}
                                        </button>
                                        <span className="ml-4 text-gray-400 text-sm">{desc}</span>
                                    </div>
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

export default CertSelect;
