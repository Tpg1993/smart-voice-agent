### 3) Architecture Diagram (Simplified & Complete)

Below is a simplified architecture diagram illustrating the core components of the Smart Voice Agent. It shows how an offline caller connects through the Telephony Layer, gets transcribed by Speech AI, reasoned about by our Core Agent Logic, and finally executes real-world tasks and saves data.

```mermaid
graph TD
    %% Define Styles
    classDef user fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef telephony fill:#ffebee,stroke:#d32f2f,stroke-width:2px;
    classDef speech fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef core fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef integrations fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef storage fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;

    %% 1. The Real World
    Caller((Customer on<br>Phone Muted)):::user

    %% 2. Telephony Sub-System
    subgraph Telephony [1. Telephony Edge Layer]
        PBX[Twilio / Asterisk PBX]:::telephony
    end

    %% 3. Speech Sub-System
    subgraph AI_Speech [2. Speech Translation Layer]
        ASR[Sarvam AI Indic-ASR<br>Speech to Text]:::speech
        TTS[Sarvam AI Indic-TTS<br>Text to Speech]:::speech
    end

    %% 4. Core Brain Sub-System
    subgraph Brain [3. Core Multi-Agent Logic]
        Router[Master Router Agent]:::core
        Specialists[Industry Specialists<br>Hotel / Salon / Edu / Clinic]:::core
    end

    %% 5. Action Sub-System
    subgraph Actions [4. Database & Integrations]
        CRM[(Business CRM)]:::integrations
        SMS[SMS & Notification Tools]:::integrations
    end

    %% 6. Storage & Auditing Sub-System
    subgraph Storage [5. Data Storage & Auditing]
        Postgres[(PostgreSQL DB)]:::storage
        Redis[(Redis Cache)]:::storage
        AudioBlob[(Audio Blob Storage)]:::storage
    end

    %% Workflow Connections
    Caller <-->|Standard Phone Call| PBX
    
    PBX -->|Audio Stream| ASR
    ASR -->|Text Utterance| Router
    
    Router -->|If specialized question| Specialists
    Specialists -->|Formulate Answer| TTS
    
    Specialists <-->|Check Booking Slots| CRM
    Specialists -->|Trigger Confirmation Text| SMS
    
    TTS -->|Play audio back| PBX

    %% Storage Connections
    Router -.->|Maintain Session State| Redis
    Specialists -.->|Maintain Session State| Redis
    Specialists -.->|Save Transcripts & Summaries| Postgres
    PBX -.->|Save Call Recording| AudioBlob
```

### Explaining the Diagram
When communicating this architecture to non-technical stakeholders, use this 5-step explanation:

1. **The Telephony Edge (Red):** The customer picks up their cell phone and makes a standard phone call. Twilio or Asterisk acts as our bridge, answering the phone call and turning it into an audio stream.
2. **Speech Translation (Orange):** We use **Sarvam AI** to act as the "Ears" and "Mouth". The ear (ASR) turns human speech into readable text for the computer. The Mouth (TTS) takes our computer's answer and speaks it in a human-like voice.
3. **Core Multi-Agent Logic (Green):** This is the actual "Brain". It reads the translated text, figures out what the user wants using the **Master Router**, and assigns the task to an **Industry Specialist** (like a Salon Agent or Hotel Agent) equipped with specialized knowledge.
4. **Database & Integrations (Purple):** The "Hands". When the brain decides it's time to book an appointment or answer a question about prices, it reaches into this layer to check real CRM databases or send follow-up text messages.
5. **Data Storage & Auditing (Yellow):** The "Memory". Everything that happens is safely recorded. Short-term memory goes to **Redis**, long-term conversation summaries go to **PostgreSQL**, and the actual audio recordings go to **Audio Blob Storage** for compliance and auditing.
