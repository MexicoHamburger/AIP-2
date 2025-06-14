import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";
import { useInputForm } from "@/InputFormStore";

const PROF_MAP: Record<string, string> = {
    "AI 지원 도구": "AI-assisted technology tool(s)",
    "자동화된 테스트": "Automated testing",
    "지속적 통합/배포 (CI/CD)": "Continuous integration (CI) and (more often) continuous delivery",
    "데브옵스 기능": "DevOps function",
    "개발자 포털": "Developer portal or other central places to find tools/services",
    "이너소스 활동": "Innersource initiative",
    "지식 공유 커뮤니티": "Knowledge sharing community",
    "마이크로서비스": "Microservices",
    "시스템 모니터링 도구": "Observability tools",
    "해당 없음": "RNone of these"
};

const ProfTech = () => {
    const navigate = useNavigate();
    const [state, dispatch] = useInputForm();
    return (
        <ReusableSkillSelect
            title="전문 분야 선택"
            description="본인의 전문 분야를 선택해주세요."
            availableSkills={[
                "AI 지원 도구",
                "자동화된 테스트",
                "지속적 통합/배포 (CI/CD)",
                "데브옵스 기능",
                "개발자 포털",
                "이너소스 활동",
                "지식 공유 커뮤니티",
                "마이크로서비스",
                "시스템 모니터링 도구",
                "해당 없음"
            ]}
            onSubmit={(selected) => {
                const mapped = selected.map(prof => PROF_MAP[prof]).filter(Boolean); // undefined 방지
                dispatch({ type: "SET_PROF", payload: mapped });
                navigate("/midresult")
            }}
        />
    );
};

export default ProfTech;
