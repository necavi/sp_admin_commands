from players.helpers import userid_from_index
from players.entity import PlayerEntity
from commands import CommandReturn
from engines.server import engine_server
from .utils import target_filter, Command, message_client


@Command("sp_kick", permission="sp.punishment.kick")
def sp_kick(source, command):
    if command.get_arg_count() == 1:
        source.message("Usage: ${purple}sp_kick ${white}<name|#userid|@filter> [reason: \"\"]")
        return CommandReturn.BLOCK
    targets = target_filter(command[1], source.index)
    if len(targets) == 0:
        source.message("No Targets found.")
    else:
        for target in targets:
            reason = " ".join([command[x] for x in range(2, command.get_arg_count())])
            engine_server.server_command("kickid {} {}\n".format(userid_from_index(target), reason))
        source.message("Kicked " + str(len(targets)) + " players.")
    return CommandReturn.BLOCK


@Command("sp_ban", permission="sp.punishment.ban")
def sp_ban(source, command):
    if command.get_arg_count() == 1:
        source.message("Usage: ${purple}sp_ban ${white}<name|#userid|@filter> [minutes: 0] [reason: \"\"]")
        return CommandReturn.BLOCK
    targets = target_filter(command[1], source.index)
    time = command[2] if command.get_arg_count() > 2 else 0
    reason = " ".join([command[x] for x in range(3, command.get_arg_count())])
    if len(targets) == 0:
        source.message("No Targets found.")
    else:
        for target in targets:
            engine_server.server_command("banid {} {}\n".format(time, userid_from_index(target)))
            engine_server.server_command("kickid {} {}\n".format(userid_from_index(target), reason))
        source.message("Banned " + str(len(targets)) + " players.")
    return CommandReturn.BLOCK

@Command("sp_unban", permission="sp.punishmnet.unban")
def sp_unban(source, command):
    if command.get_arg_count() == 1:
        source.message("Usage: ${purple}sp_unban ${white}<steamid>")
        return CommandReturn.BLOCK
    steamid = command[1]
    engine_server.server_command("removeid {}\n".format(steamid))
    return CommandReturn.BLOCK


@Command("sp_slay", permission="sp.punishment.slay")
def sp_slay(source, command):
    if command.get_arg_count() == 1:
        source.message("Usage: ${purple}sp_slay ${white}<name|#userid|@filter>")
        return CommandReturn.BLOCK
    targets = target_filter(command[1], source.index)
    if len(targets) == 0:
        source.message("No Targets found.")
    else:
        for target in targets:
            player = PlayerEntity(target)
            player.take_damage(player.health)
            message_client(player.index, "You have been slayed.")
        source.message("Slayed " + str(len(targets)) + " players.")
    return CommandReturn.BLOCK