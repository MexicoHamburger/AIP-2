import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

const WebInput = () => {
    const navigate = useNavigate();
    return (
        <ReusableSkillSelect
            title={
                <>
                    Web 스택 입력
                    <br />
                    <span className="text-xl text-blue-200">(Frontend, Backend)</span>
                </>
            }
            description="본인이 다룰 줄 아는 웹 기술 스택을 입력하세요."
            availableSkills={["ASP.NET", "ASP.NET CORE", "Angular", "AngularJS", "Django",
                "Express", "FastAPI", "Flask", "Laravel", "NestJS", "Next.js",
                "Node.js", "React", "Spring Boot", "Vue.js", "WordPress", "jQuery"]}
            onSubmit={(skills) => {
                navigate("/embedded-skills");
            }}
        />
    );
};

export default WebInput;