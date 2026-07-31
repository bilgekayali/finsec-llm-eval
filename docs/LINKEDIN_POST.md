# LinkedIn Launch Draft

Use one language version, not both in the same post unless your audience
expects bilingual content. Replace the Hugging Face line only after a real URL
exists.

## Turkish

Finans alanında bir LLM’i değerlendirmek, birkaç soruya doğru cevap verdiğini
görmekle bitmiyor.

Asıl sorular daha zor:

- Güvenilmeyen bir belge içindeki talimatı izliyor mu?
- Başka bir müşteriye ait veriyi açığa çıkarıyor mu?
- Yetki ve onay olmadan işlem aracı çağırıyor mu?
- Kaynağı olmayan bir mevzuat veya finans iddiasını kesinmiş gibi sunuyor mu?
- Riskli bir kararı doğru noktada insana devrediyor mu?

Bu soruları daha sistematik test etmek için geliştirdiğim
**FinSec-LLM-Eval** projesinin v0.2 sürüm adayını yayımladım.

Şu anda projede:

- 30 İngilizce ve 30 Türkçe olmak üzere 60 sentetik vaka,
- altı finansal AI güvenlik ve kontrol kategorisi,
- OpenAI Responses, OpenAI-uyumlu ve yerel Hugging Face adaptörleri,
- tekrar üretilebilir JSON ve Markdown raporları,
- Hugging Face veri seti ve Gradio Space için hazır paketler bulunuyor.

Önemli bir sınır koydum: Henüz gerçek model sıralaması yayımlamıyorum. Yeni 48
vaka insan incelemesinden geçmeden ve model çıktıları ayrıca denetlenmeden bir
“kazanan” ilan etmek bana doğru gelmiyor.

Repo:
https://github.com/bilgekayali/finsec-llm-eval

Finansal güvenlik, model değerlendirme veya Türkçe vaka kalibrasyonu alanında
çalışıyorsanız, teknik geri bildiriminizi özellikle duymak isterim.

## English

Evaluating an LLM for financial services takes more than checking whether it
answers a few questions correctly.

The harder questions are:

- Will it follow an instruction hidden inside an untrusted document?
- Will it disclose another client's data?
- Will it propose a transaction without verified authority and approval?
- Will it present an unsupported regulatory or financial claim as certain?
- Will it hand a consequential decision to the right human reviewer?

I built **FinSec-LLM-Eval** to make those control questions testable. The v0.2
release candidate is now public.

It includes:

- 60 synthetic cases, split evenly between English and Turkish;
- six finance-specific AI security and control categories;
- OpenAI Responses, OpenAI-compatible, and local Hugging Face adapters;
- reproducible JSON and Markdown reports;
- push-ready Hugging Face dataset and Gradio Space packages.

One deliberate limitation: I am not publishing a real-model ranking yet. The
48 new cases need human review, and model outputs need a separate audit before
a comparison would be responsible.

Repository:
https://github.com/bilgekayali/finsec-llm-eval

If you work in financial security, model evaluation, or Turkish-language
benchmarking, I would value specific technical feedback.

## Suggested first comment

The technical report explains the scoring, review gates, limitations, and why
critical failures are never hidden by an average:

https://github.com/bilgekayali/finsec-llm-eval/blob/main/docs/TECHNICAL_REPORT_v0.2.md

## Posting notes

- Do not add a model ranking until the live-run and human-review gates pass.
- Do not say the project is “production-ready,” “compliant,” or the “first”
  unless independently verified.
- A repository screenshot or a 30–45 second terminal demo is stronger than a
  generic AI-generated banner.
- Keep hashtags limited and relevant, for example:
  `#AISecurity #LLMEvaluation #FinancialServices #Cybersecurity`
