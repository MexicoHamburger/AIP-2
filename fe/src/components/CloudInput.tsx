import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

import { useInputForm } from "@/InputFormStore";


const CloudInput = () => {
  const navigate = useNavigate();
  const [state, dispatch] = useInputForm();
  return (
    <ReusableSkillSelect
      title="Cloud 스택 입력"
      description="본인이 다룰 줄 아는 클라우드 도메인을 선택하세요."
      availableSkills={["Amazon Web Services (AWS)", "Cloudflare", "Digital Ocean", "Firebase",
        "Google Cloud", "Heroku", "Microsoft Azure", "Netlify", "Vercel"]}
      onSubmit={(skills) => {
        dispatch({ type: "SET_PLAT", payload: skills });
        navigate("/web-skills");
      }}
    />
  );
};

export default CloudInput;