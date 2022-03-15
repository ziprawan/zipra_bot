async def get_perm(event: Message, chat: types.TypeInputChannel = None, user: types.TypeInputPeer = None, status: str = None):
    chat = await event.get_chat() if chat is None else chat
    user = await event.get_sender() if user is None else user
    status = await check_status(event, chat, user) if status is None else status
    if status in ['channel', 'anonch', 'anonym', 'private']:
        return None

    participant: types.channels.ChannelParticipant = await event.client(functions.channels.GetParticipantRequest(
        channel = chat,
        participant = user
    ))

    if status in ['admin', 'creator']:
        return participant.participant.admin_rights
    elif status == "member":
        chat: types.Channel = await event.get_chat()
        return chat.default_banned_rights
    elif status == "restricted":
        return participant.participant.banned_rights
    else:
        return None

# ============================================================================================================================

async def ban(event: Message, lang: Language, user: TypePeer|List[TypePeer], reason: str):
    chat = await event.get_chat()
    client: TelegramClient = event.client

    if isinstance(user, list):
        success, failed = 0, 0
        for usr in user:
            try:
                await client.edit_permissions(
                    chat,
                    usr,
                    0,
                    view_messages=False
                )
                success += 1
            except errors.UserAdminInvalidError:
                failed += 1
        return await event.reply(
            (await lang.get('restrict_batch')).format_map(Default(
                action = "Ban",
                success = str(success),
                failed = str(failed),
                reason = str(reason)
            ))
        )

    try:
        await client.edit_permissions(
            chat,
            user,
            0,
            view_messages=False
        )
    except errors.UserAdminInvalidError:
        return await event.reply(
            (await lang.get('restrict_admin_error')).format_map(Default(action="ban"))
        )
    # if ban_result.updates != []:
    #     await client.delete_messages(chat, ban_result.updates[0])
    string: str = await lang.get('banned')
    vars = ['name']
    res = [user.title if isinstance(user, Channel) else user.first_name]
    
    if reason != None:
        string += '\n' + await lang.get('reason')
        vars.append('reason')
        res.append(reason)

    offs, lens = ol_generator(string, vars, res)
    await send_sticker(
        client, 
        chat, 
        6080049489123476920, 
        -8737819976689190729, 
        b'\x02_U\xfe\x0e\x00\x00M\xb5b\x0b4\xf3\xbd\xebR\xa9\xf1<=\xac\x94nt\xebG\xe2\x08\xa9',
        "Hahahaha, got banned!",
        False)
    await event.respond(
        string.format_map(Default(name=res[0], reason=reason)),
        formatting_entities = [InputMessageEntityMentionName(
            offset = offs[0],
            length = lens[0],
            user_id = InputUser(
                user_id = user.id,
                access_hash = user.access_hash
            )
        )]
    )

# =================================================================================================================================

class Parser:
    def __init__(self, username: str, text: str) -> None:
        self.uname = username
        self.text = text

    async def get_command(self, with_uname: bool = True) -> str | None:
        teks: str = self.text # Example /start@examplebot
        if teks == None:
            return None
        uname = self.uname # examplebot
        prefix = self.prefix # Ada $ / dan ! dll
        if teks[0] in prefix:
            if '\n' in teks:
                splitted = teks.split("\n", 1)
                if ' ' in splitted[0]:
                    splitted = teks.split(' ', 1)
            else:
                splitted = teks.split(' ', 1)
            split_by_space = splitted
            split_by_prefix = split_by_space[0].split(teks[0]) # '' dan json@zipra_bot
            split_by_tag = split_by_prefix[1].split('@') # json dan zipra_bot
            if len(split_by_tag) == 1:
                if with_uname:
                    return split_by_tag[0]
                return split_by_tag[0].lower()
            if split_by_tag[1].lower() == uname or split_by_tag[1] == '':
                if with_uname:
                    return split_by_tag[0]
                return split_by_tag[0].lower() # Return 'json'
    
    async def get_options(self) -> str | None:
        tujuan = await self.get_command(False)
        pesan = self.text
        if pesan == None or tujuan == None:
            return None
        uname = self.uname
        tmp = pesan.replace(pesan[0]+tujuan, '', 1)
        print(tmp)
        split_space = pesan.split('\n') if tmp[:1] == '\n' else pesan.split(' ')
        print(split_space)
        if len(split_space) <= 1:
            return None
        else:
            for i in self.prefix:
                if i == pesan[0]:
                    perintah = split_space[0].split(i)
                    print(perintah)
                    if isinstance(tujuan, str):
                        tujuan_by_uname = f'{tujuan}@{uname}'
                        print(tujuan_by_uname)
                        if perintah[1] == tujuan or perintah[1] == tujuan_by_uname:
                            hmm = pesan.replace(split_space[0], '', 1)
                            print(hmm)
                            args = hmm.replace('\n', '', 1) if hmm[:1] == '\n' else hmm.replace(' ', '', 1)
                            print(args)
                            return args
                        else:
                            return None
                    else:
                        return None
