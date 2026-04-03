<?php
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método não permitido.']);
    exit;
}

$nome     = strip_tags(trim($_POST['nome']     ?? ''));
$email    = trim($_POST['email']    ?? '');
$telefone = strip_tags(trim($_POST['telefone'] ?? ''));
$assunto  = strip_tags(trim($_POST['assunto']  ?? ''));
$mensagem = strip_tags(trim($_POST['mensagem'] ?? ''));

if (empty($nome) || empty($email) || empty($mensagem)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Preencha todos os campos obrigatórios.']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'E-mail inválido.']);
    exit;
}

$to      = 'contato@gastaoemoukarzel.adv.br';
$subject = '=?UTF-8?B?' . base64_encode('Contato via Site — ' . $assunto) . '?=';

$body  = "Nome: {$nome}\n";
$body .= "E-mail: {$email}\n";
$body .= "Telefone: {$telefone}\n";
$body .= "Assunto: {$assunto}\n";
$body .= "\nMensagem:\n{$mensagem}\n";

$headers  = "From: site@gastaoemoukarzel.adv.br\r\n";
$headers .= "Reply-To: {$email}\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";

if (mail($to, $subject, $body, $headers)) {
    echo json_encode(['success' => true, 'message' => 'Mensagem enviada com sucesso!']);
} else {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Erro ao enviar. Tente novamente.']);
}
