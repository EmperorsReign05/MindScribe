
import { Ollama } from "npm:@langchain/community/llms/ollama";
import { PromptTemplate } from "npm:@langchain/core/prompts";
import { RunnableSequence } from "npm:@langchain/core/runnables";
import { StringOutputParser } from "npm:@langchain/core/output_parsers";
import { SupabaseVectorStore } from "npm:@langchain/community/vectorstores/supabase";
import { OllamaEmbeddings } from "npm:@langchain/community/embeddings/ollama";

app.post('/make-server-16d07a57/chat', async (c) => {
  try {
    const { messages } = await c.req.json();
    if (!messages || messages.length === 0) {
      return c.json({ error: 'Messages are required' }, 400);
    }

    // 1. Initialize models and vector store
    const llm = new Ollama({ 
      baseUrl: "http://host.docker.internal:11434", // IMPORTANT: For local dev
      model: "gemma:2b" 
    });
    const embeddings = new OllamaEmbeddings({
      baseUrl: "http://host.docker.internal:11434", // IMPORTANT: For local dev
      model: "gemma:2b"
    });

    const vectorStore = new SupabaseVectorStore(embeddings, {
      client: supabase,
      tableName: 'documents', // Assumes you have a 'documents' table with pgvector
      queryName: 'match_documents',
    });
    const retriever = vectorStore.asRetriever();

    // 2. Create a prompt template
    const prompt = PromptTemplate.fromTemplate(`
      You are MindScribe, a compassionate and supportive AI wellness companion.
      Your role is to listen, reflect, and provide gentle guidance based on established therapeutic techniques.
      Use the following retrieved context to inform your response, but prioritize a natural, caring, and conversational tone.
      Do not mention the context directly. If the context is not relevant, rely on your general training to provide a supportive response.

      CONTEXT: {context}

      CONVERSATION HISTORY:
      {chat_history}

      USER'S LATEST MESSAGE: {question}

      YOUR RESPONSE:
    `);

    // 3. Construct the RAG chain
    const chain = RunnableSequence.from([
      {
        question: (input) => input.question,
        chat_history: (input) => input.chat_history,
        context: (input) => retriever.invoke(input.question),
      },
      prompt,
      llm,
      new StringOutputParser(),
    ]);

    const question = messages[messages.length - 1].text;
    const chat_history = messages.slice(0, -1).map(m => `${m.isUser ? 'User' : 'AI'}: ${m.text}`).join('\n');

    const result = await chain.invoke({
      question,
      chat_history,
    });
    
    return c.json({ reply: result });

  } catch (error) {
    console.error('Chat endpoint error:', error);
    return c.json({ error: 'Internal server error during chat processing' }, 500);
  }
});
Deno.serve(app.fetch)