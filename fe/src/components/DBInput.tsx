import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

import { useInputForm } from "@/InputFormStore";

const DBInput = () => {
  const navigate = useNavigate();
  const [state, dispatch] = useInputForm();
  return (
    <ReusableSkillSelect
      title="DB 스택 입력"
      description="본인이 다룰 줄 아는 DB 기술 스택을 선택하세요."
      availableSkills={["Dynamodb", "Elasticsearch", "MariaDB", "Microsoft SQL Server",
        "MongoDB", "MySQL", "Oracle", "PostgreSQL", "Redis", "SQLite"]}
      onSubmit={(skills) => {
        dispatch({ type: "SET_DB", payload: skills });
        navigate("/cloud-skills");
      }}
    />
  );
};

export default DBInput;