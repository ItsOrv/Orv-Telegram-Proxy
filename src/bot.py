@client.on(events.NewMessage(chats=channels))
async def my_event_handler(event):
    message = event.message.message
    proxy_links = re.findall(r'https?://t\.me/proxy\?\S+', message)
    if proxy_links:
        for link in proxy_links:
            try:
                server = re.search(r'server=([^&]+)', link).group(1)
                port = re.search(r'port=([^&]+)', link).group(1)
                server_txt = server[:16] + '.etc' if len(server) > 16 else server

                # Ping the server
                ping = ping_server(server)

                # Skip the message if ping is not available
                if ping == "N/A":
                    logging.info(f"Skipping message with IP {server} due to N/A ping.")
                    continue

                # Get location information
                response = requests.get(f'http://ip-api.com/json/{server}')
                response.raise_for_status()
                location = response.json().get('country', 'Unknown')

                text = (
                    f"**〰️Orv〰️\n\n"
                    f"• Country: {location} \n"
                    f"• IP: {server_txt} \n"
                    f"• Port: {port} \n"
                    f"• Ping: {ping} \n\n"
                    f"**[proxy]({proxy_channel_url})~[config]({config_channel_url})~[bot]({bot_url})~[support]({support_url})"
                )
                buttons = [Button.url('Connect', link)]
                await bot.send_message(channel_id, text, buttons=buttons, link_preview=False)
            except AttributeError:
                logging.error(f"Error parsing link: {link}. Required parameters missing.")
            except requests.RequestException as e:
                logging.error(f"Error fetching data for {server}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
