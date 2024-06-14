import { UseFormRegister } from 'react-hook-form';
import {  Handle, Position, type NodeProps } from 'reactflow';

export interface InputNodeProps {
    title: string
    description: string
    placeholder: string
    hasTextArea: boolean
    id: number
    inputarea: string
    register: UseFormRegister<any>
}


export function InputNode({ data: {register, ...data} }: NodeProps<InputNodeProps>) {
    return (
        <div style={{ padding: 20, borderWidth: 4, display: 'flex', flexDirection: 'column', border: '2px solid #000000', borderRadius: 10, width: 400, height: 450, fontSize: "1.2rem" }}>
            <h2 style={{margin: "0"}}>{data.title}</h2>
            {!data.hasTextArea && <p>{data.description}</p>}
            {data.hasTextArea && <h3>🎓 Context (Optional):</h3>}
            {data.hasTextArea && <textarea
                id={"context-"+data.id.toString()}
                // placeholder={data.placeholder}
                defaultValue={data.placeholder}
                {...register("context-"+data.id.toString())}
                style={{ height: '50%', marginTop: 'auto',  resize: 'none' }}></textarea>}
            
            {data.hasTextArea && <h3>🐚 Inputs (Optional):</h3>}
            {data.hasTextArea && <textarea
                id={"inputs-"+data.id.toString()}
                // placeholder={data.inputarea}
                defaultValue={data.inputarea}
                {...register("inputs-"+data.id.toString())}
                style={{ height: '50%', marginTop: 'auto',  resize: 'none' }}></textarea>}

            <Handle type='target' id='l' position={Position.Left}  />
            <Handle type='target' id='b' position={Position.Bottom} />
            <Handle type='source' id='b' position={Position.Bottom} />
            <Handle type='source' id='r' position={Position.Right} />
        </div>
    );
}

