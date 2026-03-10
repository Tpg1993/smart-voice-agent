### 3) Architecture Diagram (Atomic Level)

```mermaid
flowchart TB
    subgraph Telephony_Layer ["1. Telephony Layer"]
        TG[Telephony/IVR Gateway]
    end

    subgraph Speech_Processing ["2. Speech & Language Center"]
        LD[Language Detection System]
        STT[Sarvam AI Indic-ASR]
        TTS[Sarvam AI Indic-TTS]
    end

    subgraph Core_Engine ["3. Core Conversation Engine (Multi-Agent System)"]
        RA["Router Module<br/>(Intent Classification)"]
        subgraph Industry_Agents
            HA[Healthcare Module]
            EA[Education Module]
            HAA[Hospitality Module]
            SA[Salon Module]
graph TD
    %% Define Styles
    classDef user fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef telephony fill:#ffebee,stroke:#d32f2f,stroke-width:2px;
    classDef speech fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef core fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef integrations fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;

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
        CRM[(Business CRM / Postgres)]:::integrations
        SMS[SMS & Notification Tools]:::integrations
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
```


*Note: Depending on scale, a background monitoring routine runs continuously to measure caller sentiment and interrupt the flow if a caller becomes highly distressed, routing them to a live human operator.*
