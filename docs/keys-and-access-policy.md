# Ключи, подписки и доступы при миграции OpenClaw → Hermes

## Коротко

Ключи не надо отправлять в чат агенту.

Лучший вариант: миграционный агент находит, **какие ключи нужны**, а человек вводит их локально в Hermes через безопасный способ.

## Три режима работы с ключами

### Режим 1. Рекомендуемый: вручную заново ввести ключи в Hermes

Подходит почти всем.

Как работает:

1. Audit находит названия ключей в OpenClaw: например `OPENROUTER_API_KEY`, `TELEGRAM_BOT_TOKEN`, `ANTHROPIC_API_KEY`.
2. В отчёте показывается только:
   - имя ключа;
   - где найден;
   - нужен ли он в Hermes;
   - куда его добавить.
3. Значение ключа не печатается.
4. Человек вводит ключ локально через Hermes setup/auth или в локальный `.env` нужного профиля.

Плюсы:

- меньше риск утечки;
- проще объяснить;
- подходит для подписчиков;
- не зависит от того, как OpenClaw хранил секреты.

Минусы:

- надо один раз руками вставить ключи.

### Режим 2. Локальный перенос ключей из OpenClaw

Только для продвинутых и только на своей машине.

Условия:

- миграция запускается локально;
- audit уже пройден;
- backup создан;
- OpenClaw gateway остановлен, если переносится Telegram;
- человек явно подтвердил перенос секретов;
- итоговый отчёт не содержит значений ключей.

Важно: даже если Hermes имеет `hermes claw migrate --migrate-secrets`, текущий локальный review нашёл safety-блокеры. Поэтому для подписчиков этот режим нельзя делать “одной кнопкой” без дополнительных защит.

### Режим 3. Запрещено: скинуть все ключи в чат

Не делать:

- отправлять `.env` в Telegram/Discord/чат агенту;
- вставлять полный OpenAI/OpenRouter/Telegram token в публичный Codex/Hermes prompt;
- загружать unredacted audit в GitHub;
- просить агента “сам найди и скопируй все ключи” без локального режима и approval.

## Как вводить разные типы доступов

### OpenAI API key

Если используется OpenAI API billing key, вводить как provider/API key в Hermes.

Не путать с ChatGPT Plus/Pro/Team.

### OpenAI Codex / ChatGPT subscription route

Если Hermes использует Codex OAuth, лучше пройти OAuth локально:

```bash
hermes auth add openai-codex --type oauth
```

или профильно:

```bash
hermes --profile <profile> auth add openai-codex --type oauth
```

### OpenRouter / Anthropic / DeepSeek / Groq / ElevenLabs

Лучший путь - добавить ключ через Hermes auth/config для нужного профиля или через profile `.env`.

Миграционный отчёт должен сказать:

```text
Нужен ключ: OPENROUTER_API_KEY
Где был найден: ~/.openclaw/.env
Куда добавить: Hermes profile <profile>
Значение: не показано
```

### Telegram bot token

Самый опасный класс.

Правило:

1. Сначала определить старого holder-а: OpenClaw gateway, старый сервис, Docker, launchd, другой Hermes profile.
2. Не запускать Hermes gateway с этим token, пока старый holder жив.
3. После cutover ждать 60-90 секунд и проверять `polling conflict`.

Для обычного человека лучше не “автокопировать Telegram token”, а показать инструкцию:

```text
1. Остановите старый OpenClaw gateway.
2. Вставьте TELEGRAM_BOT_TOKEN в Hermes profile .env или gateway setup.
3. Запустите Hermes gateway.
4. Проверьте, что нет polling conflict.
```

## Что должен показывать отчёт по ключам

Правильно:

```json
{
  "name": "TELEGRAM_BOT_TOKEN_EXAMPLE",
  "source_file": "~/.openclaw/.env",
  "present": true,
  "value_length": 46,
  "value": "[REDACTED]",
  "target_action": "manual-entry-required"
}
```

Неправильно:

```text
TELEGRAM_BOT_TOKEN -> <raw-token-value>
```

## Простая рекомендация для продукта

Для подписчиков делаем так:

- по умолчанию **не переносим ключи автоматически**;
- показываем список нужных ключей;
- даём человеку copy-paste инструкцию, куда каждый ключ вставить;
- Telegram token переносим только отдельным шагом;
- автоматический перенос секретов оставляем как advanced mode, выключенный по умолчанию.
