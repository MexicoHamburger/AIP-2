import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

const DBInput = () => {
  const navigate = useNavigate();
  return (
    <ReusableSkillSelect
      title="DB 스택 입력"
      description="본인이 다룰 줄 아는 DB 기술 스택을 선택하세요."
      availableSkills={["Dynamodb", "Elasticsearch", "MariaDB", "Microsoft SQL Server", 
        "MongoDB", "MySQL", "Oracle", "PostgreSQL", "Redis", "SQLite"]}
      onSubmit={(skills) => {
        navigate("/cloud-skills");
      }}
    />
  );
};

export default DBInput;