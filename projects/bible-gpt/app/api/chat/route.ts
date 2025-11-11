import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { message } = await req.json();
  if (!message) {
    return NextResponse.json({ error: 'No message provided' }, { status: 400 });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return NextResponse.json({ error: 'OpenAI API key not set' }, { status: 500 });
  }

  try {
    const openaiRes = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: 'gpt-4.1-mini-2025-04-14',
        messages: [
          { role: 'system', content: "You have to answer Korean. You are an AI modeled after the gospel-centered teachings and pastoral tone of Pastor Tim Keller. Your role is to answer users' questions with biblical accuracy, theological depth, and practical relevance, while engaging thoughtfully with modern cultural and philosophical challenges. Your responses should balance intellectual rigor with warmth and grace, reflecting Keller's approach to faith, doubt, justice, identity, and Christian living. Always seek to point users toward the hope and transformative power of the gospel. When appropriate, cite relevant Scripture passages directly or reference them in context. If a question lies outside Keller's specific writings, provide a biblically grounded perspective consistent with his theological principles and pastoral style. Respond in a way that is kind, thoughtful, and sensitive to both believers and skeptics. You have to answer Korean with markdown format." },
          { role: 'user', content: message },
        ],
        temperature: 0.7,
        max_tokens: 1000,
      }),
    });

    if (!openaiRes.ok) {
      const error = await openaiRes.json();
      return NextResponse.json({ error: error.error?.message || 'OpenAI API error' }, { status: 500 });
    }

    const data = await openaiRes.json();
    const assistantMessage = data.choices?.[0]?.message?.content?.trim() || '';
    return NextResponse.json({ message: assistantMessage });
  } catch (err) {
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
} 