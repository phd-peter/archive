import { NextRequest, NextResponse } from "next/server";
import { extractTranscript, generateThreadAndPost } from "@/app/actions/youtube";

export async function POST(req: NextRequest) {
  try {
    const { url, generatePost } = await req.json();
    if (!url) {
      return NextResponse.json({ error: "No URL provided" }, { status: 400 });
    }
    const docs = await extractTranscript(url);
    let thread = null;
    let post = null;
    if (generatePost) {
      const result = await generateThreadAndPost(docs);
      thread = result.thread;
      post = result.post;
    }
    return NextResponse.json({ transcript: docs, thread, post });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
} 