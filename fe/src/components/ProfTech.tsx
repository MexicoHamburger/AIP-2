import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

const ProfTech = () => {
    const navigate = useNavigate();
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
                navigate("/midresult")
            }}
        />
    );
};

export default ProfTech;
