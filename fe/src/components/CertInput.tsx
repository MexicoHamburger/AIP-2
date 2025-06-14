import CertSelect from "@/components/CertSelect";
import { useNavigate } from "react-router";
import { useInputForm } from "@/InputFormStore";

const skills = [
    { name: "IPE", desc: "정보처리기사 자격증" },
    { name: "AWS", desc: "AWS Certified, NCA, NCP 등 AWS 및 클라우드 연관 자격증" },
    { name: "DATA", desc: "ADsP, ADP, SQLD 등 데이터 분석 분야 자격증" },
    { name: "AI", desc: "AICE, AIDE, Tensorflow Developer Certificate 등 AI 관련 자격증" },
    {
        name: "Univ Award", desc: (<>
            <span className="font-bold">대학 내</span>
            {" 공모전 / 해커톤 등 직무 유관 수상이력"}
        </>)
    },
    {
        name: "Outer Award", desc: (<>
            <span className="font-bold">대학 외</span>
            {" 공모전 / 해커톤 등 직무 유관 수상이력"}
        </>)
    },
];

const CERT_MAP: Record<string, string> = {
    IPE: "CERT_IPE",
    AWS: "CERT_AWS",
    DATA: "CERT_DATA",
    AI: "CERT_AI",
    "Univ Award": "AWARD_UNIV",
    "Outer Award": "AWARD_OUTER"
};

const CertInput = () => {
    const navigate = useNavigate();
    const [state, dispatch] = useInputForm();
    return (
        <CertSelect
            title="자격증 / 수상이력"
            description="아래 목록 중 보유한 자격증 및 수상이력을 선택하세요."
            availableSkills={skills}
            onSubmit={(selected) => {
                const mapped = selected.map(item => CERT_MAP[item]).filter(Boolean);
                dispatch({ type: "SET_CERTS", payload: mapped });
                navigate("/career")
            }}
        />
    );
};

export default CertInput;
