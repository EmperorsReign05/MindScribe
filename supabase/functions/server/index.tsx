import { Hono } from "npm:hono";
import { cors } from "npm:hono/cors";
import { logger } from "npm:hono/logger";
import { createClient, SupabaseClient } from "npm:@supabase/supabase-js@2";

// LangChain Imports
import { Ollama } from "npm:@langchain/community/llms/ollama";
import { PromptTemplate } from "npm:@langchain/core/prompts";
import { SupabaseVectorStore } from "npm:@langchain/community/vectorstores/supabase";
import { OllamaEmbeddings } from "npm:@langchain/community/embeddings/ollama";
import { formatDocumentsAsString } from "npm:langchain/util/document";

const app = new Hono();

app.use('*', cors({
  origin: '*',
  allowHeaders: ['*'],
  allowMethods: ['*'],
}));

app.use('*', logger());

const supabase: SupabaseClient = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
);

// --- RAG Chat Endpoint ---
app.post('/make-server-16d07a57/chat', async (c) => {
  try {
    const { messages } = await c.req.json();
    if (!messages || messages.length === 0) {
      return c.json({ error: 'Messages are required' }, 400);
    }

    const llm = new Ollama({
      baseUrl: "http://host.docker.internal:11434",
      model: "gemma:2b"
    });
    const embeddings = new OllamaEmbeddings({
      baseUrl: "http://host.docker.internal:11434",
      model: "gemma:2b"
    });

    const vectorStore = new SupabaseVectorStore(embeddings, {
      client: supabase,
      tableName: 'documents',
      queryName: 'match_documents',
    });

    const retriever = vectorStore.asRetriever();

    const prompt = PromptTemplate.fromTemplate(`
      You are MindScribe, a compassionate AI wellness companion.
      Use the following retrieved context to inform your response in a caring, conversational tone.
      Do not mention the context directly. If it's not relevant, ignore it.

      CONTEXT: {context}
      CONVERSATION HISTORY: {chat_history}
      USER'S MESSAGE: {question}

      YOUR RESPONSE:
    `);

    const question = messages[messages.length - 1].text;
    const chat_history = messages.slice(0, -1).map((m: { isUser: boolean; text: string }) => `${m.isUser ? 'User' : 'AI'}: ${m.text}`).join('\n');

    // **DEFINITIVE FIX: A more direct and type-safe RAG implementation**
    // 1. Retrieve relevant documents from your vector store.
    const retrievedDocs = await retriever.getRelevantDocuments(question);
    const context = formatDocumentsAsString(retrievedDocs);

    // 2. Format the prompt with all the necessary information.
    const formattedPrompt = await prompt.format({
      context,
      chat_history,
      question,
    });

    // 3. Invoke the language model with the final formatted prompt.
    const result = await llm.invoke(formattedPrompt);

    return c.json({ reply: result });

  } catch (error) {
    console.error('Chat endpoint error:', error);
    return c.json({ error: 'Internal server error during chat processing' }, 500);
  }
});

// Your other endpoints can remain here

Deno.serve(app.fetch);