// src/pages/AnalyzingView.tsx
import { Loader2, CheckCircle } from "lucide-react";
import { useNavigate } from "react-router";
import { useInputForm } from "@/InputFormStore";
import { useEffect, useState } from "react";

const SKILLSET2 = [
    "JS", "TS", "HTMLCSS", "React", "VueJS", "Electron", "Next", "Nuxt", "Angular",
    "Redux", "Java", "Go", "Node", "SpringBoot", "Express", "Flask", "FastAPI", "Spring",
    "Python", "TensorFlow", "Keras", "ScikitLearn", "PyTorch", "ReactNative", "Kotlin",
    "Swift", "SQL", "PostgreSQL", "MySQL", "MongoDB", "DynamoDB", "Oracle", "Redis",
    "Pandas", "Numpy", "Docker", "DockerCompose", "Kubernetes", "Helm", "Jenkins",
    "GitLabCI", "CircleCI", "TravisCI", "AzureDevOps", "Git", "AWS", "Azure", "GCP",
    "Terraform", "Ansible", "Puppet", "Chef", "Packer", "Vagrant", "Kafka", "RabbitMQ",
    "ApacheSpark", "Prometheus", "Grafana", "ELK", "Fluentd", "OAuth2", "JWT", "SSLTLS",
    "Bash", "PowerShell"
] as const;

export const rawAlias: Record<string, string> = {
    /* 우측이 skill token으로 쓰일 애들. */
    "JavaScript": "JS",
    "TypeScript": "TS",
    "HTML/CSS": "HTMLCSS",
    "Vue.js": "VueJS",
    "Next.js": "Next",
    "Node.js": "Node",
    "Spring Boot": "SpringBoot",
    "Spring Framework": "Spring",
    "Scikit-Learn": "ScikitLearn",
    "Torch/PyTorch": "PyTorch",
    "React Native": "ReactNative",
    "Dynamodb": "DynamoDB",
    "NumPy": "Numpy",
    "Microsoft Azure": "Azure",
    "Amazon Web Services (AWS)": "AWS",
    "Apache Kafka": "Kafka",
    "Bash/Shell (all shells)": "Bash",
    // …필요 시 계속 추가
};

const setSkill2 = new Set<string>(SKILLSET2);
const normalize = (s: string) =>
    s.toLowerCase().replace(/[\s\-\._\/\(\)]+/g, "");

const aliasMap: Record<string, string> = Object.fromEntries(
    Object.entries(rawAlias).map(([k, v]) => [normalize(k), v])
);


const AnalyzingView = () => {
    const navigate = useNavigate();
    const [isDone, setIsDone] = useState(false);
    const [state, dispatch] = useInputForm();  // ← dispatch 사용!

    /* ----- 데이터 전송 & 완료 처리 ----- */
    useEffect(() => {

        let navTimer: NodeJS.Timeout;   // ⏱️ 타이머 핸들
        const sendData = async () => {
            const payload = {
                careerTokens: state.careerTokens,
                certTokens: state.certTokens,
                langTokens: state.langTokens,
                dbTokens: state.dbTokens,
                platformTokens: state.platformTokens,
                webTokens: state.webTokens,
                embTokens: state.embTokens,
                miscTokens: state.miscTokens,
                toolsTokens: state.toolsTokens,
                profTokens: state.profTokens
            };

            const mergedTokens = [
                ...state.langTokens,
                ...state.dbTokens,
                ...state.platformTokens,
                ...state.webTokens,
                ...state.embTokens,
                ...state.miscTokens,
                ...state.toolsTokens
            ];
            if (mergedTokens.includes("Git")) {
                payload.miscTokens = payload.miscTokens.filter(t => t !== "Git");
            }

            const skillsLocal = new Set<string>();
            mergedTokens.forEach(tok => {
                if (setSkill2.has(tok)) skillsLocal.add(tok);
                else {
                    const aliased = aliasMap[normalize(tok)];
                    if (aliased && setSkill2.has(aliased)) skillsLocal.add(aliased);
                }
            });
            const SKILLS_UNIQUE = [...skillsLocal];

            const firstPayload = {
                DatabaseHaveWorkedWith: payload.dbTokens ?? [],
                EmbeddedHaveWorkedWith: payload.embTokens ?? [],
                LanguageHaveWorkedWith: payload.langTokens ?? [],
                MiscTechHaveWorkedWith: payload.miscTokens ?? [],
                PlatformHaveWorkedWith: payload.platformTokens ?? [],
                ProfessionalTech: payload.profTokens ?? [],
                ToolsTechHaveWorkedWith: payload.toolsTokens ?? [],
                WebframeHaveWorkedWith: payload.webTokens ?? []
            };

            const secondPayload = [
                ...(SKILLS_UNIQUE ?? []),
                ...(payload.certTokens ?? []),
                ...(payload.careerTokens ?? [])
            ];

            console.log(firstPayload)
            console.log(secondPayload)
            const res1 = await fetch("http://localhost:5000/feat1", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ tokens: firstPayload })
            });
            const data1 = await res1.json();
            dispatch({ type: "SET_API1_RESULT", payload: data1 });

            const res2 = await fetch("http://localhost:5000/feat2/rec", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ sequence: secondPayload })
            });
            const data2 = await res2.json();
            dispatch({ type: "SET_API2_RESULT", payload: data2 });

            console.log(data1)
            console.log(data2)
        };

        setIsDone(true);
        navTimer = setTimeout(() => {             // 1초 후 이동
            navigate("/results");
        }, 1000);
        sendData();
    }, []);

    /* ----- 화면 렌더 ----- */
    return (
        <div className="min-h-screen bg-black text-white overflow-hidden">
            {/* Animated background blobs */}
            <div className="absolute inset-0">
                <div className="absolute top-20 left-10 w-72 h-72 bg-blue-600/10 rounded-full blur-3xl animate-pulse" />
                <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: "1s" }} />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-cyan-600/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: "2s" }} />
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

            {/* Main */}
            <main className="relative z-10 flex flex-col items-center justify-center pt-32">
                {isDone ? (
                    <div className="flex flex-col items-center space-y-6 animate-fade-in">
                        <CheckCircle className="h-20 w-20 text-green-400" />
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                            분석 완료!
                        </h1>
                        <p className="text-lg text-gray-300">결과 페이지로 이동 중입니다…</p>
                    </div>
                ) : (
                    <div className="flex flex-col items-center space-y-6 animate-fade-in">
                        <Loader2 className="h-20 w-20 text-blue-400 animate-spin" />
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                            분석중입니다..
                        </h1>
                        <p className="text-lg text-gray-300">잠시만 기다려 주세요.</p>
                    </div>
                )}
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

export default AnalyzingView;
