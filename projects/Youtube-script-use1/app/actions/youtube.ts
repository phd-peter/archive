import { YoutubeLoader } from "@langchain/community/document_loaders/web/youtube";
import { GoogleGenerativeAI } from "@google/generative-ai";

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

export async function extractTranscript(url: string) {
  if (!url) throw new Error("No URL provided");
  const loader = YoutubeLoader.createFromUrl(url, {
    language: "ko",
    addVideoInfo: false,
  });
  const docs = await loader.load();
  return docs;
}

export async function generateThreadAndPost(transcriptDocs: any[]) {
  if (!GEMINI_API_KEY) throw new Error("Gemini API Key not set");
  const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
  const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
  const transcriptText = transcriptDocs.map((doc: any) => doc.pageContent).join("\n\n");

  const threadPrompt = `아래 유튜브 영상 자막을 바탕으로, 스레드 게시물들(최대 500자의 글자수)을 작성해줘.\n\n- 각 스레드는 핵심 메시지나 인사이트가 잘 드러나도록 2~3문장 이내로 작성\n- 스레드 간 구분은 반드시 ---SPLIT--- 으로\n- 마크다운, 특수문자 없이 순수 텍스트만 사용하되 이모지는 포함해도 됨.\n- 첫 스레드는 영상의 주제나 핵심 메시지 요약\n- 마지막 스레드는 요약, 질문, 혹은 독자에게 생각할 거리를 던지는 문장으로 마무리\n- 너무 길거나 장황하지 않게, 읽기 쉽게\n\n자막:\n${transcriptText}`;

  const postPrompt = `아래 유튜브 영상 자막을 바탕으로, LinkedIn에 올릴 수 있는 하나의 완성된 게시글을 작성해줘.전문성이 잘 드러나도록.\n\n- 마크다운, 이모지, 특수문자 없이 순수 텍스트만 사용\n- 논리적이고 자연스럽게, 읽기 쉽게 작성\n- 영상의 핵심 메시지, 주요 인사이트, 배운 점, 느낀 점 등을 포함\n- 마지막에는 요약 또는 독자에게 생각할 거리를 던지는 문장으로 마무리\n\n자막:\n${transcriptText}`;

  const [threadResult, postResult] = await Promise.all([
    model.generateContent(threadPrompt),
    model.generateContent(postPrompt),
  ]);

  return {
    thread: threadResult.response.text(),
    post: postResult.response.text(),
  };
} 